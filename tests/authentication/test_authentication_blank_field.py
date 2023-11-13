import json

import postgres
import requests
from allure_commons._allure import description, link, step, title, feature
from hamcrest import assert_that, is_

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.queries.postgres_db import PostgresDB
from framework.tools.generator_random_data import generate_user_data
from framework.endpoints.authenticate_api import AuthenticateAPI


@feature("Authentication of user")
@link(
    url="https://github.com/Sunagatov/Online-Store/wiki/API-Specification-for-Product",
    name="Description of the tested functionality",
)
class TestAuthentication:
    @title("Test authentication, negative scenario")
    @description(
        "WHEN fields password, email are blank "
        "THEN  status HTTP CODE =  400"
    )
    def test_authentication_blank_password(self):
        with step("Generation data for registration"):
            data: dict = generate_user_data()

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(response.status_code, is_(201))

        with step("Authentication  user with blanked password"):
            " password = blank "
            data_post = {
                "email": data["email"],
                "password": " ",
            }

            print(data_post)
            response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
            assert_that(response.status_code, is_(400))
            print(response.json())
            assert_that(response.json()["message"][0],
                        is_('Password is the mandatory attribute'))


def test_authentication_blank_password_email():
    with step("Generation data for registration"):
        data: dict = generate_user_data()

    with step("Registration new user"):
        response = AuthenticateAPI().registration(body=data)
        assert_that(response.status_code, is_(201))

    with step("Authentication  user with blanked password"):
        " password = blank "
        data_post = {
            "email": " ",
            "password": " ",
        }
        response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
        assert_that(response.status_code, is_(400))


def test_authentication_blank_email():
    with step("Generation data for registration"):
        data: dict = generate_user_data()

    with step("Registration new user"):
        response = AuthenticateAPI().registration(body=data)
        assert_that(response.status_code, is_(201))

    with step("Authentication  user with blanked email"):
        data_post = {
            "email": " ",
            "password": data["password"],
        }

        print(data_post)
        response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
        assert_that(response.status_code, is_(400))
        print(response.json())
        assert_that(response.json()["message"][0],
                    is_('Email is the mandatory attribute'))
