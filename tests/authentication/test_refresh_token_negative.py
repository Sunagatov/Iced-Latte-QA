import pytest
from allure import feature, description, link, step, title
from allure import severity
from hamcrest import assert_that, is_, empty

from framework.asserts.common import assert_response_message
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import generate_jwt_token, generate_user


@feature("Refresh token")
@link(
    url="http://localhost:8083/api/docs/swagger-ui/index.html#/Security/refreshToken",
)
class TestLogout:
    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test refresh access and refresh token with expired access token")
    @description(
        "Give user registered and login in."
        "WHEN user sent request to refresh token with expired access token."
        "THEN status HTTP CODE = 401 and "
    )
    def test_refresh_access_token_with_expired_access_token(
        self, create_authorized_user
    ):
        with step("Registration and authorization of user"):
            user = create_authorized_user["user"]

        with step("Generate expired token"):
            expired_access_token = generate_jwt_token(email=user["email"], expired=True)

        with step("Verify that access token is expired by getting info about user"):
            UsersAPI().get_user(token=expired_access_token, expected_status_code=401)

        with step("Sent request for refresh access token using expired access token."):
            response_refresh_token = AuthenticateAPI().refresh_token(
                token=expired_access_token, expected_status_code=401
            )

        with step("Verify access token and refresh token are empty in response"):
            access_token_after_refresh = response_refresh_token.json().get("token", "")
            refresh_token_after_refresh = response_refresh_token.json().get(
                "refreshToken", ""
            )
            assert_that(
                access_token_after_refresh, is_(empty()), reason="Token is in response"
            )
            assert_that(
                refresh_token_after_refresh, is_(empty()), reason="Token is in response"
            )

    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test refresh access and refresh token with expired refresh token")
    @description(
        "Give user registered and login in."
        "WHEN user sent request to refresh token with expired refresh token."
        "THEN status HTTP CODE = 401 and appropriate message"
    )
    def test_refresh_access_token_with_expired_refresh_token(
        self, create_authorized_user
    ):
        with step("Registration and authorization of user"):
            user = create_authorized_user["user"]

        with step("Generate expired token"):
            expired_refresh_token = generate_jwt_token(
                email=user["email"], expired=True
            )

        with step("Verify that access token is expired by getting info about user"):
            UsersAPI().get_user(token=expired_refresh_token, expected_status_code=401)

        with step("Sent request for refresh access token using expired access token."):
            response_refresh_token = AuthenticateAPI().refresh_token(
                token=expired_refresh_token, expected_status_code=401
            )

        with step("Verify access token and refresh token are empty in response"):
            access_token_after_refresh = response_refresh_token.json().get("token", "")
            refresh_token_after_refresh = response_refresh_token.json().get(
                "refreshToken", ""
            )
            assert_that(
                access_token_after_refresh, is_(empty()), reason="Token is in response"
            )
            assert_that(
                refresh_token_after_refresh, is_(empty()), reason="Token is in response"
            )

        with step("Verify message in response"):
            expected_message = "Jwt token is expired"
            assert_response_message(
                response_refresh_token, expected_message=expected_message
            )

        with step("Verify message in response"):
            expected_message = "Jwt token is expired"
            assert_response_message(
                response_refresh_token, expected_message=expected_message
            )

    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test refresh access token and refresh token with blacklisted access token")
    @description(
        "Give user registered and login out using access token."
        "WHEN user sent request to refresh token with blacklisted access token."
        "THEN status HTTP CODE = 400 and appropriate message"
    )
    def test_refresh_access_token_with_blacklisted_access_token(
        self, create_authorized_user
    ):
        with step("Registration and authorization of user"):
            token = create_authorized_user["token"]

        with step("Log out of user"):
            logging_out_response = AuthenticateAPI().logout(token=token)
            assert_that(
                logging_out_response.status_code,
                is_(200),
                reason='Failed request "logout"',
            )

        with step(
            "Sent request for refresh access token using blacklisted access token."
        ):
            response_refresh_token = AuthenticateAPI().refresh_token(
                token=token, expected_status_code=400
            )

        with step("Verify access token and refresh token are empty in response"):
            access_token_after_refresh = response_refresh_token.json().get("token", "")
            refresh_token_after_refresh = response_refresh_token.json().get(
                "refreshToken", ""
            )
            assert_that(
                access_token_after_refresh, is_(empty()), reason="Token is in response"
            )
            assert_that(
                refresh_token_after_refresh, is_(empty()), reason="Token is in response"
            )

        with step("Verify message in response"):
            expected_message = "JWT Token is blacklisted"
            assert_response_message(
                response_refresh_token, expected_message=expected_message
            )

    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test refresh access token and refresh token with blacklisted refresh token")
    @description(
        "Give user registered and login out using refresh token."
        "WHEN user sent request to refresh token with blacklisted refresh token."
        "THEN status HTTP CODE = 400 and appropriate message"
    )
    def test_refresh_access_token_with_blacklisted_refresh_token(
        self, create_authorized_user
    ):
        with step("Registration and authorization of user"):
            token, refresh_token = (
                create_authorized_user["token"],
                create_authorized_user["refreshToken"],
            )

        with step("Log out of user with refresh token"):
            logging_out_response = AuthenticateAPI().logout(token=refresh_token)
            assert_that(
                logging_out_response.status_code,
                is_(200),
                reason='Failed request "logout"',
            )

        with step(
            "Sent request for refresh access token using blacklisted refresh token."
        ):
            response_refresh_token = AuthenticateAPI().refresh_token(
                token=refresh_token, expected_status_code=400
            )

        with step("Verify access token and refresh token are empty in response"):
            access_token_after_refresh = response_refresh_token.json().get("token", "")
            refresh_token_after_refresh = response_refresh_token.json().get(
                "refreshToken", ""
            )
            assert_that(
                access_token_after_refresh, is_(empty()), reason="Token is in response"
            )
            assert_that(
                refresh_token_after_refresh, is_(empty()), reason="Token is in response"
            )

        with step("Verify message in response"):
            expected_message = "JWT Token is blacklisted"
            assert_response_message(
                response_refresh_token, expected_message=expected_message
            )

    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test refresh access token and refresh token using empty token")
    @description(
        "WHEN user sent request to refresh access token with empty refresh token."
        "THEN status HTTP CODE = 400 and appropriate message"
    )
    def test_refresh_access_token_with_empty_refresh_token(self):
        with step("Sent request for refresh access token using empty refresh token."):
            refresh_token = ""
            response_refresh_token = AuthenticateAPI().refresh_token(
                token=refresh_token, expected_status_code=400
            )

            with step("Verify access token and refresh token are empty in response"):
                access_token_after_refresh = response_refresh_token.json().get(
                    "token", ""
                )
                refresh_token_after_refresh = response_refresh_token.json().get(
                    "refreshToken", ""
                )
                assert_that(
                    access_token_after_refresh,
                    is_(empty()),
                    reason="Token is in response",
                )
                assert_that(
                    refresh_token_after_refresh,
                    is_(empty()),
                    reason="Token is in response",
                )

            with step("Verify message in response"):
                expected_message = "Bearer authentication header is absent"
                assert_response_message(
                    response_refresh_token, expected_message=expected_message
                )

    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title(
        "Test refresh access token and refresh token using token containing not exist email in BD"
    )
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to refresh access token with token of non-existing user, "
        "THEN the response code is 404 and the response body contains the error message"
    )
    def test_refresh_access_token_with_token_containing_not_correct_user_email(self):
        with step("Sent request for refresh access token using token non exist user."):
            email_of_non_existing_user = generate_user()["email"]
            token_of_non_existing_user = generate_jwt_token(email_of_non_existing_user)
            response_refresh_token = AuthenticateAPI().refresh_token(
                token=token_of_non_existing_user, expected_status_code=404
            )

        with step("Checking the response body"):
            expected_error_message = "User with the provided email does not exist"
            assert_response_message(response_refresh_token, expected_error_message)

        with step("Verify access token and refresh token are empty in response"):
            access_token_after_refresh = response_refresh_token.json().get("token", "")
            refresh_token_after_refresh = response_refresh_token.json().get(
                "refreshToken", ""
            )
            assert_that(
                access_token_after_refresh, is_(empty()), reason="Token is in response"
            )
            assert_that(
                refresh_token_after_refresh, is_(empty()), reason="Token is in response"
            )

    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title(
        "Test refresh access token and refresh token using token not containing email"
    )
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to refresh access token with token of non-existing user, "
        "THEN the response code is 404 and the response body contains the error message"
    )
    def test_refresh_access_token_with_token_not_containing_user_email(self):
        with step(
            "Sent request for refresh access token using token not containing email."
        ):
            token_without_email = generate_jwt_token()
            response_refresh_token = AuthenticateAPI().refresh_token(
                token=token_without_email, expected_status_code=400
            )

        with step("Checking the response body"):
            expected_error_message = "User email not found in jwtToken"
            assert_response_message(response_refresh_token, expected_error_message)

        with step("Verify access token and refresh token are empty in response"):
            access_token_after_refresh = response_refresh_token.json().get("token", "")
            refresh_token_after_refresh = response_refresh_token.json().get(
                "refreshToken", ""
            )
            assert_that(
                access_token_after_refresh, is_(empty()), reason="Token is in response"
            )
            assert_that(
                refresh_token_after_refresh, is_(empty()), reason="Token is in response"
            )
