import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, is_

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.tools.generators import generate_user_data


@feature("Authentication of user")
class TestAuthentication:
    @title("Test authentication, negative scenario")
    @description(
        "GIVEN user is registered"
        "WHEN user submit invalid password, email "
        "THEN status HTTP CODE = 401"
    )
    def test_authentication_incorrect_password(self):
        with step("Generation data for registration"):
            data = generate_user_data(
                first_name_length=5, last_name_length=5, password_length=8
            )

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(
                response.status_code, is_(201), reason="Expected status code 201"
            )

        with step("Authentication  user with incorrect password"):
            data_post = {
                "email": data["email"],
                "password": data["password"] + "invalid",
            }

            response = AuthenticateAPI().authentication(
                email=data_post["email"], password=data_post["password"]
            )
            assert_that(
                response.status_code, is_(401), reason="Expected status code 401"
            )

    def test_authentication_incorrect_email(self):
        with step("Generation data for registration"):
            data = generate_user_data(
                first_name_length=5, last_name_length=5, password_length=8
            )

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(
                response.status_code, is_(201), reason="Expected status code 201"
            )

        with step("Authentication  user with incorrect email"):
            data_post = {
                "email": "fake.fake@fake.com",
                "password": data["password"],
            }
            response = AuthenticateAPI().authentication(
                email=data_post["email"], password=data_post["password"]
            )
            assert_that(
                response.status_code, is_(401), reason="Expected status code 401"
            )

    def test_authentication_incorrect_password_email(self):
        with step("Generation data for registration"):
            data = generate_user_data(
                first_name_length=5, last_name_length=5, password_length=8
            )

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(
                response.status_code, is_(201), reason="Expected status code 201"
            )

        with step("Authentication  user with incorrect password and email"):
            data_post = {
                "email": "fake.fake@fake.com",
                "password": data["password"] + "invalid",
            }
            response = AuthenticateAPI().authentication(
                email=data_post["email"], password=data_post["password"]
            )
            assert_that(
                response.status_code, is_(401), reason="Expected status code 401"
            )
