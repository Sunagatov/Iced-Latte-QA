import pytest
from allure import description, step, title, feature, severity
from hamcrest import assert_that, is_not, empty

from configs import firstName, lastName, password, email, imap_server, email_address_to_connect, gmail_password, \
    email_iced_late
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.asserts.common import assert_message_in_response, assert_response_message, assert_content_type
from framework.tools.generators import generate_user_data
from tests.conftest import UserRegistrationParams


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
    def test_confirmation_email_for_registration_with_empty_code(self, code, expected_status_code,
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
    @pytest.mark.parametrize('registration_user_with_email',
                             [UserRegistrationParams(first_name=firstName, last_name=lastName, password=password,
                                                     email=email, email_box="Inbox", key='from_',
                                                     value=email_iced_late, imap_server=imap_server,
                                                     email_address=email_address_to_connect,
                                                     gmail_password=gmail_password)], indirect=True)
    def test_confirmation_email_with_used_code(self, registration_user_with_email):
        with step("Registration user"):
            _, _, code_from_email = registration_user_with_email

        with step("Confirm email for registration with already used code"):
            code_already_used = code_from_email
            response_confirmation = AuthenticateAPI().confirmation_email(code=code_already_used,
                                                                         expected_status_code=400)
            expected_message = "Incorrect token"
            assert_response_message(response=response_confirmation, expected_message=expected_message)

