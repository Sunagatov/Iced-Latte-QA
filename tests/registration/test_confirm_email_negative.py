import pytest
from allure import description, step, title, feature, severity

from configs import email_iced_late, imap_server, email_address_to_connect, gmail_password, firstName, lastName, \
    password
from framework.asserts.common import assert_message_in_response, assert_response_message
from framework.endpoints.authenticate_api import AuthenticateAPI


@feature("Confirm email for registration with code, negative scenario")
class TestConfirmationEmail:
    @pytest.mark.medium
    @severity(severity_level="MAJOR")
    @title("Test confirmation email for user's registration with empty code")
    @description(
        "WHEN the user submits the empty code for confirmation email for registration"
        "THEN status HTTP CODE = 400 and error message"
    )
    @pytest.mark.parametrize(
        "code, expected_status_code, expected_message_part",
        [
            pytest.param(
                " ",
                400,
                "ErrorMessage: Token cannot be empty"

            ),
            pytest.param(
                "testtest",
                400,
                "Incorrect token format, token must be ###-###-###",
            ),
            pytest.param(
                "123-123-123 ", 400, "Incorrect token"
            ),
            pytest.param(
                "12345678910 ", 400, "Incorrect token format, token must be ###-###-###"
            ),
            pytest.param(
                "$*@!_+_*&%", 400, "Incorrect token format, token must be ###-###-###"
            ),
        ],
    )
    def test_confirmation_email_for_registration_with_empty_and_invalid_format_code(self, code, expected_status_code,
                                                                                    expected_message_part):
        with step("Confirm email for registration with empty code"):
            response_confirmation = AuthenticateAPI().confirmation_email(code=code, expected_status_code=400)

            assert_message_in_response(response=response_confirmation, expected_message=expected_message_part)
            # assert_response_message(response=response_confirmation, expected_message=expected_message)

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test confirmation email for registration  with already used code")
    @description(
        "WHEN the user submits for confirmation email already used code"
        "THEN status HTTP CODE = 404 and error message"
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
    def test_confirmation_email_with_used_code(self, registration_and_cleanup_user_through_api):
        with step("Registration user"):
            code_from_email = registration_and_cleanup_user_through_api['code']

        with step("Confirm email for registration with already used code"):
            code_already_used = code_from_email
            response_confirmation = AuthenticateAPI().confirmation_email(code=code_already_used,
                                                                         expected_status_code=400)
            expected_message = "Incorrect token"
            assert_response_message(response=response_confirmation, expected_message=expected_message)
