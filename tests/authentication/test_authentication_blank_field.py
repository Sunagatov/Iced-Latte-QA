from allure import description, step, title, feature
from hamcrest import assert_that, is_

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generator_random_data import generate_user_data


@feature("Authentication of user")
class TestAuthentication:
    @title("Test authentication, negative scenario")
    @description(
        "WHEN fields password, email are blank "
        "THEN status HTTP CODE = 400"
    )
    def test_authentication_blank_password(self):
        with step("Generation data for registration"):
            data = generate_user_data(length_last_name=5, length_first_name=5, password_len=8)

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(response.status_code, is_(201))

        with step("Authentication  user with blanked password"):
            " password = blank "
            data_post = {
                "email": data["email"],
                "password": " ",
            }

            response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
            assert_that(response.status_code, is_(400))

    def test_authentication_blank_password_and_email(self):
        with step("Authentication  user with blanked password"):
            " password = blank "
            data_post = {
                "email": " ",
                "password": " ",
            }
            response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
            assert_that(response.status_code, is_(400))

    def test_authentication_blank_email(self):
        with step("Generation data for registration"):
            data = generate_user_data(length_first_name=5, length_last_name=5, password_len=8)

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(response.status_code, is_(201))

        with step("Authentication  user with blanked email"):
            data_post = {
                "email": " ",
                "password": data["password"],
            }

            response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
            assert_that(response.status_code, is_(400))
