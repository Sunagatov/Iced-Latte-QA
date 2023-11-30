from allure import title, step
from psycopg2 import connect
from pytest import fixture

from configs import DB_NAME, HOST_DB, PORT_DB, DB_USER, DB_PASS
from framework.queries.postgres_db import PostgresDB
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_user

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
