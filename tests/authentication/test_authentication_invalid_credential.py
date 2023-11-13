import json

import postgres
import requests
from allure_commons._allure import description, link, step, title, feature
from hamcrest import assert_that, is_

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.queries.postgres_db import PostgresDB
from framework.tools.generator_random_data import generate_user_data
from framework.endpoints.authenticate_api import AuthenticateAPI

postgresBD = PostgresDB()


@feature("Authentication of user")
@link(
    url="https://github.com/Sunagatov/Online-Store/wiki/API-Specification-for-Product",
    name="Description of the tested functionality",
)
class TestAuthentication:
    @title("Test authentication, negative scenario")
    @description(
        "WHEN user submit invalid password, email "
        "THEN  status HTTP CODE =  401"
    )
    def test_authentication_incorrect_password(self):
        with step("Generation data for registration"):
            data: dict = generate_user_data()

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
            assert_that(response.json()["message"][0], is_(f"Invalid credentials for user's account with email = '{email}'"))

    def test_authentication_incorrect_email(self):
        with step("Generation data for registration"):
            data: dict = generate_user_data()

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(response.status_code, is_(201))

        with step("Authentication  user with incorrect email"):
            " add fake email  "

            data_post = {
                "email": 'fake.fake@fake.com',
                "password": data["password"],
            }
            email = data_post["email"]
            response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
            assert_that(response.status_code, is_(401))
            assert_that(response.json()["message"][0],
                        is_(f"Bad credentials. User with the email = '{email}' does not exist"))
            print(response.json())

    def test_authentication_incorrect_password_login(self):
        with step("Generation data for registration"):
            data: dict = generate_user_data()

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


