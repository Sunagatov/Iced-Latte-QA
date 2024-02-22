import pytest
from allure import description, step, title, feature
from allure import severity
from hamcrest import assert_that, is_

from framework.asserts.common import assert_response_message, assert_content_type
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import generate_password, generate_string, generate_numeric_password, \
    generate_jwt_token, generate_user


@feature("Change user password")
class TestChangePassword:
    @pytest.mark.xfail(
        reason="BUG password accept more than 128 characters. According to requirements it should be 8-128. "
    )
    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password with less than 8 characters and more than 128 characters")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password with less than 8 characters or more than 128 characters "
        "THEN status HTTP CODE = 400, and error message is returned"
    )
    @pytest.mark.parametrize("new_password, expected_message", [
        pytest.param(generate_password(7), "Password should have a length between 8 and 128 characters"),
        pytest.param(generate_password(6), "Password should have a length between 8 and 128 characters"),
        pytest.param(generate_password(129), "Password should have a length between 8 and 128 characters"),
        pytest.param(generate_password(130), "Password should have a length between 8 and 128 characters"),
        pytest.param(generate_password(1), "Password should have a length between 8 and 128 characters"),
    ])
    def test_change_user_password_with_incorrect_length(self, create_authorized_user, new_password, expected_message):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Change user password"):
            response_changing_password = UsersAPI().change_password(token=token, old_password=user["password"],
                                                        new_password=new_password,
                                                        expected_status_code=400)

        with step("Checking the response type of the body"):
            assert_content_type(response_changing_password, "application/json")

        with step("Verify that password not successfully changes by"
                  " sent request for Authentication with new password "):
            AuthenticateAPI().authentication(email=user["email"], password=new_password, expected_status_code=401)

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password that do not meet the requirements."
           )
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password "
        "with password that empty or do not contains at least one letters or at least one digit in the password"
        "THEN status HTTP CODE = 400, and error message is returned"
    )
    @pytest.mark.parametrize("new_password, expected_message", [pytest.param(generate_string(8),
                                                                             "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&"),
                                                                pytest.param(generate_string(9),
                                                                             "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&"),
                                                                pytest.param(generate_numeric_password(length=8),
                                                                             "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&"),
                                                                pytest.param(generate_numeric_password(length=9),
                                                                             "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&"),
                                                                pytest.param(f"{generate_numeric_password(length=7)}!",
                                                                             "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&"),
                                                                pytest.param(f"{generate_string(7)}@",
                                                                             "Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&"),
                                                                pytest.param("@$!%*?&",
                                                                             'Password must be at least 8 characters long and contain at least one letter, one digit, and may include special characters @$!%*?&'),
                                                                ])
    def test_change_user_password_with_incorrect_format(self, create_authorized_user, new_password, expected_message):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Change user password"):
            response_change_password = UsersAPI().change_password(token=token, old_password=user["password"],
                                                                  new_password=new_password,
                                                                  expected_status_code=400)

        with step("Checking the response type of the body"):
            assert_content_type(response_change_password, "application/json")

        with step("Verify that password not successfully changes by"
                  " sent request for Authentication with new password "):
            AuthenticateAPI().authentication(email=user["email"], password=new_password, expected_status_code=401)

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password with empty password")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password with empty field old password or new password "
        "and both empty fields"
        "THEN status HTTP CODE = 400, and error message is returned"
    )
    @pytest.mark.parametrize("new_password, old_password, expected_message", [
        pytest.param("", None, "Password is the mandatory attribute"),
        pytest.param(None, "", " "),
        pytest.param("", "", " ")
    ])
    def test_change_user_password_with_empty_fields(self, create_authorized_user, new_password, old_password,
                                                    expected_message):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Change user password"):
            new_password = generate_password(8) if new_password is None else new_password
            old_password = user["password"] if old_password is None else old_password

            response_change_password = UsersAPI().change_password(token=token, old_password=old_password,
                                                                  new_password=new_password,
                                                                  expected_status_code=400)

        with step("Checking the response type of the body"):
            assert_content_type(response_change_password, "application/json")

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password with incorrect old password.")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password with incorrect old password "
        "THEN status HTTP CODE = 401, and error message is returned"
    )
    def test_change_user_password_with_incorrect_old_password(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Change user password"):
            new_password = generate_password(8)
            response_change_password = UsersAPI().change_password(token=token,
                                                                  old_password=user["password"] + "incorrect",
                                                                  new_password=new_password,
                                                                  expected_status_code=401)

        with step("Verify response message"):
            email = user["email"]
            expected_message = f"User with userEmail = '{email}' provided incorrect password."
            assert_response_message(response=response_change_password, expected_message=expected_message)

        with step("Checking the response type of the body"):
            assert_content_type(response_change_password, "application/json")

        with step("Verify that password not successfully changes by"
                  " sent request for Authentication with new password "):
            AuthenticateAPI().authentication(email=user["email"], password=new_password, expected_status_code=401)

    @pytest.mark.xfail(reason="Bug in API?? Http status code 500")
    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password with invalid token.")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password with invalid token "
        "THEN status HTTP CODE = 400, and error message is returned"
    )
    def test_change_user_password_with_invalid_token(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], "invalid_token"

        with step("Change user password"):
            new_password = generate_password(8)
            response_change_password = UsersAPI().change_password(token=token,
                                                                  old_password=user["password"],
                                                                  new_password=new_password,
                                                                  expected_status_code=400)

        with step("Verify response message"):
            email = user["email"]
            expected_message = f"User with userEmail = '{email}' provided incorrect password."
            assert_response_message(response=response_change_password, expected_message=expected_message)

        with step("Checking the response type of the body"):
            assert_content_type(response_change_password, "application/json")

        with step("Verify that password not successfully changes by"
                  " sent request for Authentication with new password "):
            AuthenticateAPI().authentication(email=user["email"], password=new_password, expected_status_code=401)

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password with expired token.")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password with expired token "
        "THEN status HTTP CODE = 401, and error message is returned"
    )
    def test_change_user_password_with_expired_token(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Change user password"):
            expired_token = generate_jwt_token(email=user["email"], expired=True)
            new_password = generate_password(8)
            response_change_password = UsersAPI().change_password(token=expired_token,
                                                                  old_password=user["password"],
                                                                  new_password=new_password,
                                                                  expected_status_code=401)

        with step("Verify response message"):
            expected_message = "Jwt token is expired"
            assert_response_message(response=response_change_password, expected_message=expected_message)

        # with step("Checking the response type of the body"):
        #     assert_content_type(response_change_password, "application/json")

        with step("Verify that password not successfully changes by"
                  " sent request for Authentication with new password "):
            AuthenticateAPI().authentication(email=user["email"], password=new_password, expected_status_code=401)

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password with blacklisted token.")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password with blacklisted token "
        "THEN status HTTP CODE = 400, and error message is returned"
    )
    def test_change_user_password_with_blacklisted_token(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Logging out of user"):
            logging_out_response = AuthenticateAPI().logout(token=token)
            assert_that(
                logging_out_response.status_code,
                is_(200),
                reason='Failed request "logout"',
            )

        with step("Change user password"):
            new_password = generate_password(8)
            response_change_password = UsersAPI().change_password(token=token,
                                                                  old_password=user["password"],
                                                                  new_password=new_password,
                                                                  expected_status_code=400)

        with step("Verify response message"):
            expected_message = "JWT Token is blacklisted"
            assert_response_message(response=response_change_password, expected_message=expected_message)

        # with step("Checking the response type of the body"):
        #     assert_content_type(response_change_password, "application/json")

        with step("Verify that password not successfully changes by"
                  " sent request for Authentication with new password "):
            AuthenticateAPI().authentication(email=user["email"], password=new_password, expected_status_code=401)

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password with empty token.")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password with empty token "
        "THEN status HTTP CODE = 400, and error message is returned"
    )
    def test_change_user_password_with_empty_token(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Change user password"):
            new_password = generate_password(8)
            response_change_password = UsersAPI().change_password(token='',
                                                                  old_password=user["password"],
                                                                  new_password=new_password,
                                                                  expected_status_code=400)

        with step("Verify response message"):
            expected_message = "Bearer authentication header is absent"
            assert_response_message(response=response_change_password, expected_message=expected_message)

        # with step("Checking the response type of the body"):
        #     assert_content_type(response_change_password, "application/json")

        with step("Verify that password not successfully changes by"
                  " sent request for Authentication with new password "):
            AuthenticateAPI().authentication(email=user["email"], password=new_password, expected_status_code=401)

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password with token not containing email.")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password with token not containing email "
        "THEN status HTTP CODE = 400, and error message is returned"
    )
    def test_change_user_password_with_token_not_containing_email(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Change user password"):
            token_without_email = generate_jwt_token()
            new_password = generate_password(8)
            response_change_password = UsersAPI().change_password(token=token_without_email,
                                                                  old_password=user["password"],
                                                                  new_password=new_password,
                                                                  expected_status_code=400)

        with step("Verify response message"):
            expected_message = "User email not found in jwtToken"
            assert_response_message(response=response_change_password, expected_message=expected_message)

        # with step("Checking the response type of the body"):
        #     assert_content_type(response_change_password, "application/json")

        with step("Verify that password not successfully changes by"
                  " sent request for Authentication with new password "):
            AuthenticateAPI().authentication(email=user["email"], password=new_password, expected_status_code=401)

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test change user's password with token containing not exist user email.")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to change password with token containing not exist user email "
        "THEN status HTTP CODE = 404, and error message is returned"
    )
    def test_change_user_password_with_token_containing_not_exist_user_email(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Change user password"):
            email_of_non_existing_user = generate_user()["email"]
            token_of_non_existing_user = generate_jwt_token(email_of_non_existing_user)
            new_password = generate_password(8)
            response_change_password = UsersAPI().change_password(token=token_of_non_existing_user,
                                                                  old_password=user["password"],
                                                                  new_password=new_password,
                                                                  expected_status_code=404)

        with step("Verify response message"):
            expected_message = "User with the provided email does not exist"
            assert_response_message(response=response_change_password, expected_message=expected_message)
        # bug: content_type = ""
        # with step("Checking the response type of the body"):
        #     assert_content_type(response_change_password, "application/json")

        with step("Verify that password not successfully changes by"
                  " sent request for Authentication with new password "):
            AuthenticateAPI().authentication(email=user["email"], password=new_password, expected_status_code=401)
