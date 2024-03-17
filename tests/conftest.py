from allure import title, step
from hamcrest import assert_that, is_, is_not, empty, not_
from psycopg2 import connect
from pytest import fixture
from assertpy import assert_that
import pytest

from configs import DB_NAME, HOST_DB, PORT_DB, DB_USER, DB_PASS, EMAIL_LOCAL_PART, EMAIL_DOMAIN
from data.data_for_cart import data_for_adding_product_to_cart
from framework.asserts.registration_asserts import check_mapping_api_to_db
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI
from framework.queries.postgres_db import PostgresDB
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_user, generate_user_data, append_random_to_local_part_email
from framework.asserts.common import assert_content_type
from framework.tools.methods_to_cart import assert_product_to_add_matches_response, \
    get_product_info
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
    """Creating and authorizing a user via API """
    with step("Generation data for registration"):
        data = generate_user_data(
            first_name_length=8, last_name_length=8, password_length=8
        )

    with step("Registration new user"):
        response_registration = AuthenticateAPI().registration(body=data)

        assert_that(
            response_registration.status_code, is_(201), reason="Expected status code 201"
        )
        token = response_registration.json()["token"]

    with step("Getting user's info via API"):
        getting_user_response = UsersAPI().get_user(token=token)
        new_user_id = getting_user_response.json()["id"]

    yield token, new_user_id

    with step("Deleting user"):
        UsersAPI().delete_user(token=token)


@fixture(scope='function')
def creating_and_adding_product_to_shopping_cart(create_authorized_user):
    with step("Registration of user"):
        user, token = create_authorized_user["user"], create_authorized_user["token"]

    with step("Getting user's info via API"):
        getting_user_response = UsersAPI().get_user(token=token)
        new_user_id = getting_user_response.json()["id"]

    with step("Get shopping cart of user and verify that user doesn't have items in shopping cart"):
        response_get_cart = CartAPI().get_user_cart(token=token)
        data = response_get_cart.json()
        assert_that(data).contains("items")
        assert_that(len(data["items"])).is_equal_to(0)

    with step("Generation data for adding to the shopping cart"):
        items_to_add = data_for_adding_product_to_cart

    with step("Adding new product to a shopping cart "):
        CartAPI().add_item_to_cart(token=token,
                                   items=items_to_add)

    with step("Checking: 1. The shopping cart created under new user. 2.Added products are in a shopping cart"):
        response_get_cart_after_added = CartAPI().get_user_cart(token=token)
        expected_user_id_in_cart = response_get_cart_after_added.json()["userId"]
        assert_that(expected_user_id_in_cart, 'Expected user ID does not match.').is_equal_to(
            new_user_id)
        product_list_after_added = get_product_info(response=response_get_cart_after_added)
        assert_product_to_add_matches_response(items_to_add, product_list_after_added)
        assert_content_type(response_get_cart, "application/json")

        yield token, new_user_id, response_get_cart_after_added


@pytest.fixture
def product_quantity(request):
    return request.param


@fixture(scope='function')
def add_product_to_favorite_list(create_authorized_user, product_quantity):
    with step("Registration of user"):
        user, token = create_authorized_user["user"], create_authorized_user["token"]

    with step("Getting all products via API"):
        response_get_product = ProductAPI().get_all()

    with step("Select and ddd random products to favorite"):
        product_list_to_favorite = extract_random_product_ids(response_get_product, product_quantity=product_quantity)
        response_add_to_favorite = FavoriteAPI().add_favorites(token=token,
                                                               favorite_product=product_list_to_favorite)
        assert_added_product_in_favorites(response_add_to_favorite, product_list_to_favorite)

    yield token, product_list_to_favorite


@pytest.fixture
def registration_and_cleanup_user_through_api(request):
    email_random = append_random_to_local_part_email(domain=EMAIL_DOMAIN, email_local_part=EMAIL_LOCAL_PART,
                                                     length_random_part=5)
    data_for_registration = {
        "firstName": request.param['firstName'],
        "lastName": request.param['lastName'],
        "password": request.param['password'],
        "email": email_random
    }

    with step("Registration new user"):
        response_registration = AuthenticateAPI().registration(body=data_for_registration)
        expected_content_type = "text/plain;charset=UTF-8"
        assert_content_type(response_registration, expected_content_type=expected_content_type)

    with step("Extract code from email for confirmation registration"):
        email_box = "Inbox"
        key = 'from_'
        value = request.param['email_iced_late']
        imap_server = request.param['imap_server']
        email_address_to_connect = request.param['email_address_to_connect']
        gmail_password = request.param['gmail_password']

        code_from_email = Email(imap_server=imap_server, email_address=email_address_to_connect,
                                mail_password=gmail_password).extract_confirmation_code_from_email(email_box=email_box,
                                                                                                   key=key, value=value)
        assert_that(code_from_email, not_(None))

    with step("Confirm registration using code from email"):
        response_after_confirmation = AuthenticateAPI().confirmation_email(code=code_from_email)

    with step("Verify that user is successfully registered by authentication through user's credentials"):
        email_for_authentication = data_for_registration["email"]
        password_for_authentication = data_for_registration["password"]

        response_authentication = AuthenticateAPI().authentication(
            email=email_for_authentication, password=password_for_authentication
        )
        expected_content_type = "application/json"
        assert_content_type(response_authentication, expected_content_type=expected_content_type)
        token = response_authentication.json().get("token")
        assert_that(token, is_not(empty()))

    yield {"user": data_for_registration, "token": response_after_confirmation.json().get("token"),
           "code": code_from_email}

    with step("Deleting user"):
        UsersAPI().delete_user(token=response_after_confirmation.json().get("token"))
