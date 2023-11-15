from allure import description, step, title, feature
from hamcrest import assert_that, is_

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generator_random_data import generate_user_data


@feature("Authentication of user")
class TestAuthentication:
    @title("Test authentication, negative scenario")
    @description(
        "WHEN user submit invalid password, email "
        "THEN status HTTP CODE = 401"
    )
    def test_authentication_incorrect_password(self):
        with step("Generation data for registration"):
            data = generate_user_data(length_first_name=5, length_last_name=5, password_len=8)

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(response.status_code, is_(201))

        with step("Authentication  user with incorrect password"):
            "add to the password in the end str 'invalid' "
            data_post = {
                "email": data["email"],
                "password": data["password"] + 'invalid',
            }

            response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
            assert_that(response.status_code, is_(401))

    def test_authentication_incorrect_email(self):
        with step("Generation data for registration"):
            data = generate_user_data(length_first_name=5, length_last_name=5, password_len=8)

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(response.status_code, is_(201))

        with step("Authentication  user with incorrect email"):
            " add fake email  "

            data_post = {
                "email": 'fake.fake@fake.com',
                "password": data["password"],
            }

            response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
            assert_that(response.status_code, is_(401))
            print(response.json())

    def test_authentication_incorrect_password_login(self):
        with step("Generation data for registration"):
            data = generate_user_data(length_last_name=5, length_first_name=5, password_len=8)

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(response.status_code, is_(201))

        with step("Authentication  user with incorrect password"):
            "add to the password in the end str 'invalid and fake email' "
            data_post = {
                "email": 'fake.fake@fake.com',
                "password": data["password"] + 'invalid',
            }
            response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
            assert_that(response.status_code, is_(401))
