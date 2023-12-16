import requests
from allure import title, step
from hamcrest import assert_that, is_
from psycopg2 import connect
from pytest import fixture

from configs import DB_NAME, HOST_DB, PORT_DB, DB_USER, DB_PASS, HOST, data_for_adding_product_to_cart
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI
from framework.queries.postgres_db import PostgresDB
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_user, generate_user_data
from framework.tools.logging import log_request
from framework.asserts.common import assert_response_message, assert_content_type
from framework.tools.methods_to_cart import assert_compare_product_to_add_with_response, \
    get_product_info, get_item_id

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
    postgres.create_user(user)
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

    yield {"user": user_to_create, "token": token}

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
def creating_and_adding_product_to_shopping_cart(create_and_delete_user_via_api):
    with step("Registration of user"):
        token, new_user_id = create_and_delete_user_via_api

    with step("Get shopping cart of user and verify that user doesn't have a shopping cart"):
        response_get_cart = CartAPI().get_user_cart(token=token, expected_status_code=404)

    with step("Checking the response body and the Content-Type"):
        expected_message = f'The shopping cart for the user with id = {new_user_id} is not found.'
        assert_response_message(response_get_cart, expected_message)
        assert_content_type(response_get_cart, "application/json")

    with step("Generation data for adding to the shopping cart"):
        items_to_add = data_for_adding_product_to_cart

    with step("Adding new product to a shopping cart "):
        CartAPI().add_new_item_to_cart(token=token,
                                       items=items_to_add)

    with step("Checking: 1. The shopping cart created under new user. 2.Added products are in a shopping cart"):
        response_get_cart_after_added = CartAPI().get_user_cart(token=token)
        expected_user_id_in_cart = response_get_cart_after_added.json()["userId"]
        assert_that(expected_user_id_in_cart), is_(new_user_id)
        product_list_after_added = get_product_info(response=response_get_cart_after_added)
        assert_compare_product_to_add_with_response(items_to_add, product_list_after_added)
        assert_content_type(response_get_cart, "application/json")

        yield token, new_user_id, response_get_cart_after_added
