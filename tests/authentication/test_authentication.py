import pytest
from allure import description, step, title, feature
from allure import severity
from hamcrest import assert_that, is_not, empty, is_

from configs import (
    email_iced_late,
    imap_server,
    email_address_to_connect,
    gmail_password,
    firstName,
    lastName,
    password,
)
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI


@feature("Authentication of user")
class TestAuthentication:
    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test authentication")
    @description(
        "GIVEN user is registered"
        "WHEN user submit valid credential for authentication"
        "THEN status HTTP CODE = 200 and get JWT token"
    )
    @pytest.mark.parametrize(
        "registration_and_cleanup_user_through_api",
        [
            {
                "firstName": firstName,
                "lastName": lastName,
                "password": password,
                "email_iced_late": email_iced_late,
                "imap_server": imap_server,
                "email_address_to_connect": email_address_to_connect,
                "gmail_password": gmail_password,
            }
        ],
        indirect=True,
    )
    def test_authentication(self, registration_and_cleanup_user_through_api):
        with step("Registration user"):
            data_for_registration = registration_and_cleanup_user_through_api["user"]

        with step("Authentication  user"):
            data_post = {
                "email": data_for_registration["email"],
                "password": data_for_registration["password"],
            }
            response = AuthenticateAPI().authentication(
                email=data_post["email"], password=data_post["password"]
            )

        with step("Assert Response JSON  have a 'token' key"):
            token = response.json().get("token")
            assert_that(token, is_not(empty()))

        with step("Validation token by retrieving user information via API request"):
            response = UsersAPI().get_user(token=token)
            assert_that(
                response.status_code, is_(200), reason="Expected status code 200"
            )
