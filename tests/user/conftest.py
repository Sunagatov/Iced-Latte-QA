import pytest
from allure_commons._allure import step

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_user


@pytest.fixture
def create_user(postgres):
    """Fixture for creating a user (not authorized)

    Args:
        postgres: fixture for working with the database
    """

    with step("Creating user via DB"):
        user_to_create = generate_user()
        postgres.insert_user(user_to_create)

    return user_to_create


@pytest.fixture
def create_authorized_user(postgres):
    """Fixture for creating an authorized user

    Args:
        postgres: fixture for working with the database
    """

    with step("Creating user via DB"):
        user_to_create = generate_user()
        postgres.insert_user(user_to_create)

    with step("Authentication of user and getting token"):
        token = \
            AuthenticateAPI().authentication(email=user_to_create['email'], password=user_to_create['password']).json()[
                "token"]

    return {"user": user_to_create, "token": token}
