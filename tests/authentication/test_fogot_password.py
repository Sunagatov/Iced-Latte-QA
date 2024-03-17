import pytest
from allure import feature, description, link, step, title
from allure import severity
from hamcrest import assert_that, is_, not_, empty, is_not
from assertpy import assert_that as assertpy_assert_that

from configs import email_iced_late, imap_server, email_address_to_connect, gmail_password, firstName, lastName, \
    password
from framework.asserts.common import assert_content_type, assert_response_message
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.class_email import Email
from framework.tools.generators import faker


@feature("Forgot password")
@link(
    url="http://localhost:8083/api/docs/swagger-ui/index.html#/Security/forgotPassword",
)
class TestForgotPassword:
    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test forgot password")
    @description(
        "Give user registered."
        "WHEN user sent request to reset password."
        "THEN status HTTP CODE = 200 "
    )
    @pytest.mark.parametrize('registration_and_cleanup_user_through_api', [{
        'firstName': firstName,
        'lastName': lastName,
        'password': password,
        'email_iced_late': email_iced_late,
        'imap_server': imap_server,
        'email_address_to_connect': email_address_to_connect,
        'gmail_password': gmail_password
    }], indirect=True)
    def test_forgot_password(self, registration_and_cleanup_user_through_api):
        with step("Registration user"):
            user = registration_and_cleanup_user_through_api["user"]
            email = user["email"]

        with step("Sent request to reset password"):
            response_to_reset_password = AuthenticateAPI().forgot_password(email=email)
            assert_that(response_to_reset_password.status_code, is_(200))

        with step("Verify reset code successfully delivered to user's email"):
            email_box = "Inbox"
            key = 'from_'
            value = email_iced_late
            code_from_email = Email(imap_server=imap_server, email_address=email_address_to_connect,
                                    mail_password=gmail_password).extract_confirmation_code_from_email(
                email_box=email_box,
                key=key, value=value)
            assertpy_assert_that(code_from_email).is_not_empty()

    @pytest.mark.xfail(reason="HTTP CODE - 400 but got 401. Error message not correct according to requirement")
    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test forgot password, sent request to reset password with invalid/empty email")
    @description(
        "Give user registered."
        "WHEN user sent request to reset password with invalid format email, or empty email field."
        "THEN status HTTP CODE = 400, and error message")
    @pytest.mark.parametrize("email_to_reset_password, expected_message", [
        pytest.param("", "Email is the mandatory attribute"),
        pytest.param("example.gmail.com", "Email must be valid"),
        pytest.param("sernamegmail.com", "Email must be valid"),
        pytest.param("sername@", "Email must be valid"),
        pytest.param("john doe@example.com", "Email must be valid"),
        pytest.param("user!name@example.com", "Email must be valid"),
        pytest.param("@gmail.com", "Email must be valid"),
        pytest.param("username@example", "Email must be valid"),
        pytest.param("user@name@example.com", "Email must be valid"),
        pytest.param(".username@example.com", "Email must be valid"),
        pytest.param("username@example_gmail.com", "Email must be valid")
    ])
    def test_forgot_password_email_not_valid(self, email_to_reset_password, expected_message):
        with step("Sent request to reset password with invalid email"):
            response_to_reset_password = AuthenticateAPI().forgot_password(email=email_to_reset_password,
                                                                           expected_status_code=400)
            assert_response_message(response=response_to_reset_password, expected_message=expected_message)
            assert_content_type(response_to_reset_password, "application/json")

    @pytest.mark.xfail(reason="Error message not correct")
    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test forgot password, send request to reset password with not exist email")
    @description(
        "Give user registered."
        "WHEN user sent request to reset password with not exist email in BD."
        "THEN status HTTP CODE = 401, and error message")
    def test_forgot_password_email_not_exist(self):
        with step("Sent request to reset password with not exist email in BD"):
            email_not_exist = faker.email()
            response_to_reset_password = AuthenticateAPI().forgot_password(email=email_not_exist,
                                                                           expected_status_code=401)
            expected_message = "Email must be valid"
            assert_response_message(response=response_to_reset_password, expected_message=expected_message)
            assert_content_type(response_to_reset_password, "application/json")
