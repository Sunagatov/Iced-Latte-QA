import requests
from allure import title, step
from hamcrest import assert_that, is_
from psycopg2 import connect
from pytest import fixture

from configs import DB_NAME, HOST_DB, PORT_DB, DB_USER, DB_PASS, HOST
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI
from framework.queries.postgres_db import PostgresDB
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_user, generate_user_data
from framework.tools.logging import log_request

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
