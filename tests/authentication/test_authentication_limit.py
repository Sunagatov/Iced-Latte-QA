from allure import description, feature, step, title
from hamcrest import assert_that, is_, none

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.steps.registration_steps import RegistrationSteps
from framework.tools.generators import generate_string
from framework.tools.matcher import is_timestamp_valid

LIMIT_ATTEMPTS = 5
DURATION_BLOCKING_MINUTES = 30
TIMESTAMP_PATTERN = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"


@feature("Authentication of user")
class TestAuthentication:
    @title("Failed authentication is limited in number")
    @description(
        f"WHEN a user enters authentication data incorrectly more than {LIMIT_ATTEMPTS} times, "
        "THEN the service blocks the user for authentication"
    )
    def test_of_limitation_attempts(self):
        with step("SetUp. Generation data of test user for registration"):
            email = generate_string(length=2, additional_characters=["@te.st"])
            first_name = generate_string(length=2)
            last_name = generate_string(length=2)
            password = generate_string(
                length=8, additional_characters=["@1"]
            ).capitalize()
            invalid_password = password + "_invalid"

            body = RegistrationSteps().data_for_sent(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

        with step("SetUp. Registration of test user"):
            registration_response = AuthenticateAPI().registration(body=body)
            assert_that(
                registration_response.status_code,
                is_(200),
                reason="Registration failed",
            )

        with step("User authentication attempt allowed number of times"):
            for attempt in range(LIMIT_ATTEMPTS):
                with step(f"Attempt {attempt}"):
                    response = AuthenticateAPI().authentication(
                        email=email, password=invalid_password
                    )
                    response_authentication = response.json()
                    assert_that(
                        response.status_code, is_(401), reason="Invalid status code"
                    )
                    assert_that(
                        response_authentication["message"],
                        is_(
                            f"Invalid credentials for user's account with email = '{email}'"
                        ),
                        reason="Authentication passed. There must be a mistake",
                    )
                    assert_that(
                        response_authentication["httpStatusCode"],
                        is_(401),
                        reason="Invalid status code in body of response",
                    )
                    assert_that(
                        is_timestamp_valid(
                            response_authentication["timestamp"], TIMESTAMP_PATTERN
                        ),
                        reason=f"Timestamp '{response_authentication['timestamp']}' does not match "
                        f"the expected format YYYY-MM-DD HH:MM:SS",
                    )

        with step("Authentication attempt over the limit"):
            response = AuthenticateAPI().authentication(
                email=email, password=invalid_password
            )
            response_locked_authentication = response.json()
            assert_that(response.status_code, is_(401), reason="Invalid status code")
            assert_that(
                response_locked_authentication["message"],
                is_(
                    f"The request was rejected due to an incorrect number of login attempts for the user "
                    f"with email='{email}'. Try again in {DURATION_BLOCKING_MINUTES} minutes or reset your password"
                ),
                reason="Authentication passed. There must be a mistake",
            )
            assert_that(
                response_locked_authentication["httpStatusCode"],
                is_(401),
                reason="Invalid status code in body of response",
            )
            assert_that(
                is_timestamp_valid(
                    response_locked_authentication["timestamp"], TIMESTAMP_PATTERN
                ),
                reason=f"Timestamp '{response_locked_authentication['timestamp']}' does not match "
                f"the expected format YYYY-MM-DD HH:MM:SS",
            )
