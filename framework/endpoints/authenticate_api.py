import json
from typing import Optional

import requests
from requests import Response

from configs import HOST
from framework.asserts.common import assert_status_code, assert_content_type
from framework.tools.logging_allure import log_request


class AuthenticateAPI:
    def __init__(self):
        """Initializing parameters for request"""
        self.url = HOST + "/api/v1/auth"
        self.headers = {"Content-Type": "application/json"}

    def authentication(self, email: str, password: str, expected_status_code: int = 200) -> Response:
        """Endpoint for authentication of user

        Args:
            expected_status_code: expected http status code from response
            email:    user's email address;
            password: password for email.
        """
        data = {
            "email": email,
            "password": password,
        }
        path = self.url + "/authenticate"
        response = requests.post(url=path, data=json.dumps(data), headers=self.headers)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response

    def logout(self, token: str) -> Response:
        """User logout

        Args:
            token: JWT token for authorization of request
        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = self.url + "/logout"
        response = requests.post(url=path, headers=headers)
        log_request(response)

        return response

    def registration(self, body: dict, expected_status_code=200) -> Response:
        """Endpoint for registration of user

        Args:
            expected_status_code: expected http status code from response
            body:   registration data with required fields:
                        email:      electronic mail;
                        firstName:  name;
                        lastName:   surname;
                        password:   password for electronic mail.
        """
        path = self.url + "/register"
        response = requests.post(url=path, data=json.dumps(body), headers=self.headers)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response

    def confirmation_email(self, code: str, expected_status_code: int = 201) -> Response:
        """Endpoint for authentication of user

        Args:
            expected_status_code: expected http status code from response
            code: confirmation code from email
        """
        data = {
            "token": code
        }
        path = self.url + "/confirm"
        response = requests.post(url=path, data=json.dumps(data), headers=self.headers)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response
