import pytest
from allure_commons._allure import step

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_user


def generate_and_insert_user(postgres):
    user = generate_user()
    postgres.create_user(user)
    return user


@pytest.fixture
def create_user(postgres):
    """Fixture for creating a user (not authorized)

    Args:
        postgres: fixture for working with the database
    """

    with step("Creating user via DB"):
        user_to_create = generate_and_insert_user(postgres)

    yield user_to_create
    postgres.delete_user(user_to_create["id"])


@pytest.fixture
def create_authorized_user(postgres):
    """Fixture for creating an authorized user

    Args:
        postgres: fixture for working with the database
    """

    with step("Creating user in DB"):
        user_to_create = generate_and_insert_user(postgres)

    with step("Authentication of user and getting token"):
        authentication_response = AuthenticateAPI().authentication(
            email=user_to_create['email'],
            password=user_to_create['password']
        )
        token = authentication_response.json()["token"]

    yield {"user": user_to_create, "token": token}

    with step("Removing user from DB"):
        postgres.delete_user(user_to_create["id"])
