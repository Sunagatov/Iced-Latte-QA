import pytest
from allure import description, step, title, feature
from allure import severity
from hamcrest import assert_that, is_, is_not, empty

from data_for_auth import firstName, lastName, password, email, email_iced_late, imap_server, email_address_to_connect, \
    gmail_password
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from tests.conftest import UserRegistrationParams


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
    @pytest.mark.parametrize('registration_user_with_email',
                             [UserRegistrationParams(first_name=firstName, last_name=lastName, password=password,
                                                     email=email, email_box="Inbox", key='from_',
                                                     value=email_iced_late, imap_server=imap_server,
                                                     email_address=email_address_to_connect,
                                                     gmail_password=gmail_password)], indirect=True)
    def test_authentication(self, registration_user_with_email):
        with step("Registration user"):
            data, _, _ = registration_user_with_email

        with step("Authentication  user"):
            data_post = {
                "email": data["email"],
                "password": data["password"],
            }
            response = AuthenticateAPI().authentication(
                email=data_post["email"], password=data_post["password"]
            )

        with step("Assert Response JSON  have a 'token' key"):
            token = response.json().get("token")
            assert_that(token, is_not(empty()))

        with step(
                "Validation token by retrieving user information via API request"
        ):
            response = UsersAPI().get_user(token=token)
            assert_that(
                response.status_code, is_(200), reason="Expected status code 200"
            )

