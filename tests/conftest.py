import time

from allure import title, step
from hamcrest import assert_that, is_, is_not, empty, not_
from psycopg2 import connect
from pytest import fixture

# from assertpy import assert_that
from assertpy import assert_that as assertpy_assert_that
import pytest

from configs import (
    DB_NAME,
    HOST_DB,
    PORT_DB,
    DB_USER,
    DB_PASS,
    EMAIL_LOCAL_PART,
    EMAIL_DOMAIN,
    EMAIL_DOMAIN2,
    EMAIL_LOCAL_PART2,
)
from data.data_for_cart import data_for_adding_product_to_cart
from framework.asserts.registration_asserts import check_mapping_api_to_db
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI
from framework.queries.postgres_db import PostgresDB
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import (
    generate_user,
    generate_user_data,
    append_random_to_local_part_email,
)
from framework.asserts.common import assert_content_type
from framework.tools.methods_to_cart import (
    assert_product_to_add_matches_response,
    get_product_info,
)
from framework.tools.class_email import Email
from framework.endpoints.product_api import ProductAPI
from framework.tools.favorite_methods import extract_random_product_ids
from framework.endpoints.favorite_api import FavoriteAPI
from framework.asserts.assert_favorite import assert_added_product_in_favorites

# Connection configuration
PostgresDB.dbname = DB_NAME
PostgresDB.host = HOST_DB
PostgresDB.port = PORT_DB
PostgresDB.user = DB_USER
PostgresDB.password = DB_PASS


@title("SetUp and TearDown connect to Postgres DataBase for testing")
@fixture(scope="function")
def postgres() -> connect:
    """Connect to Postgres DataBase"""
    with step("SetUp. Connecting to Postgres database"):
        conn = PostgresDB()

    yield conn

    with step("TearDown. Closing connect to Postgres database"):
        conn.close()


def generate_and_insert_user(postgres):
    """Generating and inserting a user into the database

    Args:
        postgres: connection to Postgres DataBase
    """

    user = generate_user()

    key_mapping = {
        "firstName": "first_name",
        "lastName": "last_name",
        "birthDate": "birth_date",
        "phoneNumber": "phone_number",
        "stripeCustomerToken": "stripe_customer_token",
    }
    user_to_insert = {key_mapping.get(k, k): v for k, v in user.items()}

    postgres.create_user(user_to_insert)

    return user


@title("Creating a user (not authorized)")
@fixture(scope="function")
def create_user(postgres):
    """Creating a user (not authorized)

    Args:
        postgres: connection to Postgres DataBase
    """

    with step("Creating user via DB"):
        user_to_create = generate_and_insert_user(postgres)

    yield user_to_create

    with step("Removing user from DB"):
        postgres.delete_user(user_to_create["id"])


@title("Creating an authorized user")
@fixture(scope="function")
def create_authorized_user(postgres):
    """Creating and authorizing a user

    Args:
        postgres: connection to Postgres DataBase
    """

    with step("Creating user in DB"):
        user_to_create = generate_and_insert_user(postgres)

    with step("Authentication of user and getting token"):
        authentication_response = AuthenticateAPI().authentication(
            email=user_to_create["email"], password=user_to_create["password"]
        )
        token = authentication_response.json()["token"]
        refresh_token = authentication_response.json()["refreshToken"]

    yield {"user": user_to_create, "token": token, "refreshToken": refresh_token}

    with step("Removing user from DB"):
        postgres.delete_user(user_to_create["id"])


@fixture(scope="function")
def create_and_delete_user_via_api():
    """Creating and authorizing a user via API"""
    with step("Generation data for registration"):
        data = generate_user_data(
            first_name_length=8, last_name_length=8, password_length=8
        )

    with step("Registration new user"):
        response_registration = AuthenticateAPI().registration(body=data)

        assert_that(
            response_registration.status_code,
            is_(201),
            reason="Expected status code 201",
        )
        token = response_registration.json()["token"]

    with step("Getting user's info via API"):
        getting_user_response = UsersAPI().get_user(token=token)
        new_user_id = getting_user_response.json()["id"]

    yield token, new_user_id

    with step("Deleting user"):
        UsersAPI().delete_user(token=token)


@fixture(scope="function")
def creating_and_adding_product_to_shopping_cart(create_authorized_user):
    """
     Fixture to create a user, add a product to their cart.

    Creates a user, gets their ID and token, adds a product to their
    shopping cart, and returns the token, user ID, and cart response.

    Args:
       create_authorized_user: Fixture returning a new authorized user
           and their token.

    Returns:
       token: New user's authentication token.
       new_user_id: New user's ID.
       response_get_cart_after_added: Response after adding product
           to cart."""
    with step("Registration of user"):
        user, token = create_authorized_user["user"], create_authorized_user["token"]

    with step("Getting user's info via API"):
        getting_user_response = UsersAPI().get_user(token=token)
        new_user_id = getting_user_response.json()["id"]

    with step(
        "Get shopping cart of user and verify that user doesn't have items in shopping cart"
    ):
        response_get_cart = CartAPI().get_user_cart(token=token)
        data = response_get_cart.json()
        assertpy_assert_that(data).contains("items")
        assertpy_assert_that(len(data["items"])).is_equal_to(0)

    with step("Generation data for adding to the shopping cart"):
        items_to_add = data_for_adding_product_to_cart

    with step("Adding new product to a shopping cart "):
        CartAPI().add_item_to_cart(token=token, items=items_to_add)

    with step(
        "Checking: 1. The shopping cart created under new user. 2.Added products are in a shopping cart"
    ):
        response_get_cart_after_added = CartAPI().get_user_cart(token=token)
        expected_user_id_in_cart = response_get_cart_after_added.json()["userId"]
        assertpy_assert_that(
            expected_user_id_in_cart, "Expected user ID does not match."
        ).is_equal_to(new_user_id)
        product_list_after_added = get_product_info(
            response=response_get_cart_after_added
        )
        assert_product_to_add_matches_response(items_to_add, product_list_after_added)

        yield token, new_user_id, response_get_cart_after_added


@pytest.fixture
def product_quantity(request):
    return request.param


@fixture(scope="function")
def add_product_to_favorite_list(create_authorized_user, product_quantity):
    """
    Adds random products to a user's favorites list.

    Registers a new user, gets all products via API, selects random
    products, adds them to the user's favorites list, and verifies they
    were added successfully.

    Args:
        create_authorized_user: Fixture that registers a new user and
            returns their auth token.
        product_quantity: Number of products to add to favorites.

    Returns:
        token: New user's auth token.
        product_list_to_favorite: List of product IDs added to favorites."""

    with step("Registration of user"):
        user, token = create_authorized_user["user"], create_authorized_user["token"]

    with step("Getting all products via API"):
        response_get_product = ProductAPI().get_all()

    with step("Select and ddd random products to favorite"):
        product_list_to_favorite = extract_random_product_ids(
            response_get_product, product_quantity=product_quantity
        )
        response_add_to_favorite = FavoriteAPI().add_favorites(
            token=token, favorite_product=product_list_to_favorite
        )
        assert_added_product_in_favorites(
            response_add_to_favorite, product_list_to_favorite
        )

    yield token, product_list_to_favorite


@pytest.fixture
def registration_and_cleanup_user_through_api(request):
    with step("Prepare data for registration"):
        email_random = append_random_to_local_part_email(
            domain=EMAIL_DOMAIN, email_local_part=EMAIL_LOCAL_PART, length_random_part=5
        )
        data_for_registration = {
            "firstName": request.param["firstName"],
            "lastName": request.param["lastName"],
            "password": request.param["password"],
            "email": email_random,
        }

    with step("Registration new user"):
        AuthenticateAPI().registration(body=data_for_registration)

    with step("Extract code from email for confirmation registration"):
        email_box = "Inbox"
        key = "from_"
        value = request.param["email_iced_late"]
        imap_server = request.param["imap_server"]
        email_address_to_connect = request.param["email_address_to_connect"]
        gmail_password = request.param["gmail_password"]

        code_from_email = Email(
            imap_server=imap_server,
            email_address=email_address_to_connect,
            mail_password=gmail_password,
        ).extract_confirmation_code_from_email(
            email_box=email_box, key=key, value=value
        )
        assert_that(code_from_email, is_not(None), "Code should not be empty")

    with step("Confirm registration using code from email"):
        response_after_confirmation_registration = AuthenticateAPI().confirmation_email(
            code=code_from_email
        )

    with step("Verify JWT token is returned after confirmation and content type"):
        assert_that(
            response_after_confirmation_registration.json()["token"], is_not(empty())
        )

    yield {
        "user": data_for_registration,
        "token": response_after_confirmation_registration.json().get("token"),
        "code": code_from_email,
    }

    with step("Deleting user"):
        UsersAPI().delete_user(
            token=response_after_confirmation_registration.json().get("token")
        )


@pytest.fixture
def register_user_and_reset_password(request):
    email_random = append_random_to_local_part_email(
        domain=EMAIL_DOMAIN2, email_local_part=EMAIL_LOCAL_PART2, length_random_part=5
    )
    data_for_registration = {
        "firstName": request.param["firstName"],
        "lastName": request.param["lastName"],
        "password": request.param["password"],
        "email": email_random,
    }

    with step("Registration new user"):
        AuthenticateAPI().registration(body=data_for_registration)

    with step("Extract code from email for confirmation registration"):
        email_box = "Inbox"
        key = "from_"
        value = request.param["email_iced_late"]
        imap_server = request.param["imap_server"]
        email_address_to_connect = request.param["email_address_to_connect"]
        gmail_password = request.param["gmail_password"]

        code_registration_from_email = Email(
            imap_server=imap_server,
            email_address=email_address_to_connect,
            mail_password=gmail_password,
        ).extract_confirmation_code_from_email(
            email_box=email_box, key=key, value=value
        )
        assert_that(
            code_registration_from_email, not_(None), "Code should not be empty"
        )

    with step("Confirm registration using code from email"):
        response_after_confirmation_registration = AuthenticateAPI().confirmation_email(
            code=code_registration_from_email
        )

    with step("Verify JWT token is returned after confirmation and content type"):
        assert_that(
            response_after_confirmation_registration.json()["token"], is_not(empty())
        )

    with step("Sent request to reset password"):
        email_to_reset_password = data_for_registration["email"]
        AuthenticateAPI().forgot_password(email=email_to_reset_password)

    with step("Verify reset code successfully delivered to user's email"):
        email_box = "Inbox"
        key = "from_"
        value = request.param["email_iced_late"]
        code_reset_from_email = Email(
            imap_server=imap_server,
            email_address=email_address_to_connect,
            mail_password=gmail_password,
        ).extract_confirmation_code_from_email(
            email_box=email_box, key=key, value=value
        )

        assert_that(code_reset_from_email, not_(None), "Code should not be empty")

    yield {
        "user": data_for_registration,
        "token": response_after_confirmation_registration.json().get("token"),
        "code": code_reset_from_email,
    }

    with step("Deleting user"):
        UsersAPI().delete_user(
            token=response_after_confirmation_registration.json().get("token")
        )
