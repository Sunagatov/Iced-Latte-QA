import pytest
from allure import description, step, title, feature
from hamcrest.core import assert_that, is_
from hamcrest.library import contains_string

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_user_data
from framework.tools.matcher import is_timestamp_valid
from tests.conftest import create_authorized_user

TIMESTAMP_PATTERN = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"


@feature("Authentication of user")
class TestAuthentication:
    @title("Test authentication, negative scenario")
    @description(
        "GIVEN user is registered"
        "WHEN fields password, email are blank "
        "THEN status HTTP CODE = 400"
    )
    @pytest.mark.parametrize(
        "email, password, expected_status_code, expected_message_part",
        [
            pytest.param(
                " ",
                " ",
                400,
                "Email is the mandatory attribute",
            ),
            pytest.param(
                None,
                " ",
                400,
                "Password is the mandatory attribute",
            ),
            pytest.param(" ", None, 400, "Email is the mandatory attribute"),
        ],
    )
    def test_authentication_with_various_blank_inputs(
        self,
        email: str,
        password: str,
        expected_status_code: int,
        expected_message_part: str,
        create_authorized_user,
    ):
        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )
        with step("Preparation data for authentication request"):
            email = user["email"] if email is None else email
            password = user["password"] if password is None else password

        with step("Authentication user with given credentials"):
            response = AuthenticateAPI().authentication(
                email=email, password=password, expected_status_code=400
            )

        with step(
            "Verify the response contains the expected part of message, http status code,and "
            "correct format of the timestamp"
        ):
            response_body = response.json()
            actual_status_code = response.status_code
            actual_message = response_body.get("message", "")
            actual_timestamp = response_body.get("timestamp", "")

            assert_that(
                actual_message,
                contains_string(expected_message_part),
                reason=f"Expected response contains '{expected_message_part}', found: '{actual_message}'",
            )
            assert_that(
                response.status_code,
                is_(expected_status_code),
                reason=f"Expected HTTP status code '{expected_status_code}', found: '{actual_status_code}'",
            )
            assert_that(
                is_timestamp_valid(actual_timestamp, TIMESTAMP_PATTERN),
                reason=f"Timestamp '{actual_timestamp}' does not match the expected format YYYY-MM-DD HH:MM:SS",
            )
