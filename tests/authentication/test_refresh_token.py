import pytest
from allure import feature, description, link, step, title
from allure import severity
from hamcrest import assert_that, is_, empty, is_not

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import generate_jwt_token


@feature("Refresh token")
@link(
    url="http://localhost:8083/api/docs/swagger-ui/index.html#/Security/refreshToken",
)
class TestLogout:
    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test refresh access token  and refresh with refresh token")
    @description(
        "Give user registered and login in."
        "WHEN access token is  expired and user sent request to refresh access token with refreshToken."
        "THEN status HTTP CODE = 200 and get JWT refresh token and access token"
    )
    def test_refresh_access_token_with_valid_refresh_token(self, create_authorized_user):
        with step("Registration of user"):
            user, access_token, token_sent_for_refresh = create_authorized_user["user"], create_authorized_user[
                "token"], \
                create_authorized_user["refreshToken"]

        with step("Generate expired token"):
            expired_access_token = generate_jwt_token(email=user["email"], expired=True)

        with step("Verify that access token is expired by getting info about user"):
            UsersAPI().get_user(token=expired_access_token, expected_status_code=401)

        with step("Sent request for refresh access token using refresh token."):
            response_refresh_token = AuthenticateAPI().refresh_token(token=token_sent_for_refresh)

        with step("Verify access token and refresh token in response"):
            access_token_after_refresh = response_refresh_token.json().get("token", '')
            refresh_token_after_refresh = response_refresh_token.json().get("refreshToken", '')
            assert_that(access_token_after_refresh, is_not(empty()), reason="Token is not in response")
            assert_that(refresh_token_after_refresh, is_not(empty()), reason="Token is not in response")

        with step("Verify that access token and refresh token are valid after refresh by getting user's info"):
            UsersAPI().get_user(token=access_token_after_refresh, expected_status_code=200)
            UsersAPI().get_user(token=refresh_token_after_refresh, expected_status_code=200)

    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test refresh access token and refresh with access token")
    @description(
        "Give user registered and login in."
        "WHEN user sent request to refresh access token with access token."
        "THEN status HTTP CODE = 200 and get JWT refresh token and access token"
    )
    def test_refresh_access_token_with_valid_access_token(self, create_authorized_user):
        with step("Registration of user"):
            user, access_token, token_sent_for_refresh = create_authorized_user["user"], create_authorized_user[
                "token"], \
                create_authorized_user["refreshToken"]

        with step("Sent request for refresh access token using access token."):
            response_refresh_token = AuthenticateAPI().refresh_token(token=access_token)

        with step("Verify access token and refresh token in response"):
            access_token_after_refresh = response_refresh_token.json().get("token", '')
            refresh_token_after_refresh = response_refresh_token.json().get("refreshToken", '')
            assert_that(access_token_after_refresh, is_not(empty()), reason="Token is not in response")
            assert_that(refresh_token_after_refresh, is_not(empty()), reason="Token is not in response")

        with step("Verify that access token and refresh token are valid after refresh by getting user's info"):
            UsersAPI().get_user(token=access_token_after_refresh, expected_status_code=200)
            UsersAPI().get_user(token=refresh_token_after_refresh, expected_status_code=200)
