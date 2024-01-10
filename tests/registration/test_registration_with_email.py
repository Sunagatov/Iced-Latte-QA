import json

import requests
from allure import description, step, title, feature
from hamcrest import assert_that, not_, is_

from configs import gmail_password, imap_server, email_address
from configs import password, firstName, lastName, gmail_address
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.class_email import Email


@feature("Registration of user")
class TestAuthentication:
    @title("Test registration with email")
    @description(
        "WHEN the user submits the minimum required data for registration,"
        "WHEN registration's confirmation code from email is provided"
        "THEN status HTTP CODE = 200 and get JWT token"
    )
    def test_authentication(self):
        with step("Generation data for registration"):
            data = {
                "firstName": firstName,
                "lastName": lastName,
                "password": password,
                "email": gmail_address,
            }

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(
                response.status_code, is_(200), reason="Expected status code 201"
            )

        with step("Extract code from email for confirmation registration"):
            email_box = "Inbox"
            key = 'FROM'
            value = 'youricedlatteshop@gmail.com'
            token = Email(imap_server=imap_server, email_address=email_address,
                          gmail_password=gmail_password).extract_confirmation_code_from_email(email_box=email_box,
                                                                                              key=key, value=value)
            assert_that(token, not_(None), "Token should not be empty")

        with step("Confirm registration using code from email"):
            data_confirm = {
                "token": f"{token}"
            }

            response = requests.post(headers={"Content-Type": "application/json"},
                                     url='http://dev.api.it-sl.ru/api/v1/auth/confirm',
                                     data=json.dumps(data_confirm))

            assert_that(
                response.status_code, is_(201), reason="Expected status code 201"
            )

        with step("Verify that user is successfully registered"):
            data_post = {
                "email": data["email"],
                "password": data["password"],
            }
            response = AuthenticateAPI().authentication(
                email=data_post["email"], password=data_post["password"]
            )
            assert_that(
                response.status_code, is_(200), reason="Expected status code 200"
            )
            token = response.json().get("token")

        with step("Deleting user"):
            UsersAPI().delete_user(token=token)
