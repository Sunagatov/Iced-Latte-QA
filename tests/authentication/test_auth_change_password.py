import pytest
from allure import feature, description, link, step, title
from allure import severity

from configs import (
    email_iced_late,
    firstName2,
    lastName2,
    password2,
    imap_server2,
    email_address_to_connect2,
    gmail_password2,
)
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_password


@feature("Reset password")
@link(
    url="http://localhost:8083/api/docs/swagger-ui/index.html#/Security/changePassword",
)
class TestResetPassword:
    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test change password through reset password")
    @description(
        "Give user registered."
        "WHEN user sent request to change password."
        "THEN status HTTP CODE = 200 "
    )
    @pytest.mark.parametrize(
        "register_user_and_reset_password",
        [
            {
                "firstName": firstName2,
                "lastName": lastName2,
                "password": password2,
                "email_iced_late": email_iced_late,
                "imap_server": imap_server2,
                "email_address_to_connect": email_address_to_connect2,
                "gmail_password": gmail_password2,
            }
        ],
        indirect=True,
    )
    def test_change_password_through_reset_password(
        self, register_user_and_reset_password
    ):
        with step("Registration user"):
            user = register_user_and_reset_password["user"]
            email = user["email"]

            code_for_reset_password = register_user_and_reset_password["code"]

        with step("Sent request to reset password"):
            new_password = generate_password(8)
            AuthenticateAPI().change_password_through_reset(
                email=email,
                code_for_reset_password=code_for_reset_password,
                new_password=new_password,
            )

        with step(
            "Verify password reset successfully by Authorization request with new password"
        ):
            AuthenticateAPI().authentication(
                email=email, password=new_password, expected_status_code=200
            )
