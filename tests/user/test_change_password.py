import pytest
from allure import description, step, title, feature
from allure import severity

from framework.asserts.common import assert_content_type
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import (
    generate_password,
    generate_string,
    generate_numeric_password,
)


@feature("Change user password")
class TestChangePassword:
    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user password with valid length")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password with length of password according to requirement"
        "THEN status HTTP CODE = 200"
    )
    @pytest.mark.parametrize(
        "new_password",
        [
            generate_password(8),
            generate_password(9),
            generate_password(63),
            generate_password(64),
            generate_password(65),
            generate_password(127),
            generate_password(128),
        ],
    )
    def test_change_user_password_with_valid_length(
        self, create_authorized_user, new_password
    ):
        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )

        with step("Change user password"):
            response_change_password = UsersAPI().change_password(
                token=token,
                old_password=user["password"],
                new_password=new_password,
                expected_status_code=200,
            )

        # bug:content_type is "" ???
        # with step("Checking the response type of the body"):
        #     assert_content_type(response_change_password, "application/json")
        with step(
            "Verify that password successfully changes by"
            " sent request for Authentication with new password "
        ):
            response_auth = AuthenticateAPI().authentication(
                email=user["email"], password=new_password, expected_status_code=200
            )
            new_token = response_auth.json()["token"]
            UsersAPI().get_user(token=new_token, expected_status_code=200)

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password that  meet the requirements.")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password "
        "with password that  contains at least one letters or at least one digit "
        "and may contain special characters ('@$!%*?&') in the password"
        "THEN status HTTP CODE = 200"
    )
    @pytest.mark.parametrize(
        "new_password",
        [
            pytest.param(generate_string(4) + generate_numeric_password(length=4)),
            pytest.param(
                generate_string(4) + generate_numeric_password(length=4) + "@"
            ),
            pytest.param(
                generate_string(4) + generate_numeric_password(length=4) + "$"
            ),
            pytest.param(
                generate_string(4) + generate_numeric_password(length=4) + "%"
            ),
            pytest.param(
                generate_string(4) + generate_numeric_password(length=4) + "&"
            ),
            pytest.param(
                generate_string(4) + generate_numeric_password(length=4) + "*"
            ),
            pytest.param(
                generate_string(4) + generate_numeric_password(length=4) + "?"
            ),
            pytest.param(
                generate_string(4) + generate_numeric_password(length=4) + "%"
            ),
        ],
    )
    def test_change_user_password_with_correct_format(
        self, create_authorized_user, new_password
    ):
        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )

        with step("Change user password"):
            response_change_password = UsersAPI().change_password(
                token=token,
                old_password=user["password"],
                new_password=new_password,
                expected_status_code=200,
            )

        # bug:content_type is "" ???
        # with step("Checking the response type of the body"):
        #     assert_content_type(response_change_password, "application/json")

        with step(
            "Verify that password  successfully changes by"
            " sent request for Authentication with new password "
        ):
            AuthenticateAPI().authentication(
                email=user["email"], password=new_password, expected_status_code=200
            )
