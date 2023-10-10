from allure import title, step
from psycopg2 import connect
from pytest import fixture

from configs import DB_NAME, HOST_DB, PORT_DB, DB_USER, DB_PASS
from framework.queries.postgres_db import PostgresDB

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
