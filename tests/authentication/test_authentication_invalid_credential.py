import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, is_

from framework.asserts.common import assert_response_message
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_user_data
from tests.conftest import create_authorized_user


@pytest.mark.critical
@feature("Authentication of user")
class TestAuthentication:
    @title("Test authentication, negative scenario")
    @description(
        "GIVEN user is registered"
        "WHEN user submit invalid password, email "
        "THEN status HTTP CODE = 401"
    )
    def test_authentication_incorrect_password(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Authentication  user with incorrect email"):
            data_post = {
                "email": user["email"],
                "password": user["password"] + "invalid",
            }
            response_authentication = AuthenticateAPI().authentication(
                email=data_post["email"], password=data_post["password"], expected_status_code=401
            )
        with step("Verify error message from response"):
            expected_message = f"Invalid credentials for user's account with email = '{data_post['email']}'"
            assert_response_message(response=response_authentication, expected_message=expected_message)

    def test_authentication_incorrect_email(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Authentication  user with incorrect email"):
            data_post = {
                "email": user["email"] + "_invalid",
                "password": user["password"],
            }
            response_authentication = AuthenticateAPI().authentication(
                email=data_post["email"], password=data_post["password"], expected_status_code=401
            )
        with step("Verify error message from response"):
            expected_message = f"Invalid credentials for user's account with email = '{data_post['email']}'"
            assert_response_message(response=response_authentication, expected_message=expected_message)

    def test_authentication_incorrect_password_email(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Authentication  user with incorrect email"):
            data_post = {
                "email": user["email"] + "_invalid",
                "password": user["password"] + "invalid",
            }
            response_authentication = AuthenticateAPI().authentication(
                email=data_post["email"], password=data_post["password"], expected_status_code=401
            )
        with step("Verify error message from response"):
            expected_message = f"Invalid credentials for user's account with email = '{data_post['email']}'"
            assert_response_message(response=response_authentication, expected_message=expected_message)