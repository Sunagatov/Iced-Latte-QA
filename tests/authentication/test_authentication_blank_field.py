import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, is_, contains_string
import re

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_user_data

timestamp_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"


@feature("Authentication of user")
class TestAuthentication:
    @title("Test authentication, negative scenario")
    @description(
        "GIVEN user is registered"
        "WHEN fields password, email are blank "
        "THEN status HTTP CODE = 400"
    )
    @pytest.mark.parametrize("email, password, expected_status_code, expected_message_part", [
        (" ", " ", 400, "Email is the mandatory attribute"),
        (None, " ", 400, "Password is the mandatory attribute"),
        (" ", None, 400, "Email is the mandatory attribute")
    ], ids=["password_and_email_blank", "password_blank", "email_blank"])
    def test_authentication_with_various_blank_inputs(self, email, password, expected_status_code, expected_message_part):
        with step("Generation data for registration"):
            data = generate_user_data(length_first_name=5, length_last_name=5, password_len=8)

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(response.status_code, is_(201), reason='Expected status code 201')

        with step("Preparation data for authentication request"):
            "Generated email/password if the parameter is None"
            email = data["email"] if email is None else email
            password = data["password"] if password is None else password

        with step("Authentication user with given credentials"):
            response = AuthenticateAPI().authentication(email=email, password=password)

        with step("Verify the response contains the expected part of message, http status code,and "
                  "correct format of the timestamp"):
            response_body = response.json()
            actual_status_code = response.status_code
            actual_message = response_body.get("message", "")
            actual_timestamp = response_body.get("timestamp", "")
            time_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"

            assert_that(actual_message, contains_string(expected_message_part),
                        reason=f"Expected response contains '{expected_message_part}', found: '{actual_message}'")
            assert_that(response.status_code, is_(expected_status_code),
                        reason=f"Expected HTTP status code '{expected_status_code}', found: '{actual_status_code}'")
            assert re.match(time_pattern, actual_timestamp), \
                f"Timestamp '{actual_timestamp}' does not match the expected format YYYY-MM-DD HH:MM:SS"
