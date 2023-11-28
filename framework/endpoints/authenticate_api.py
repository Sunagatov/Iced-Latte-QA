import json

import requests
from requests import Response

from configs import HOST
from framework.tools.logging import log_request


class AuthenticateAPI:
    def __init__(self):
        """Initializing parameters for request"""
        self.url = HOST + "/api/v1/auth"
        self.headers = {"Content-Type": "application/json"}

    def authentication(self, email: str, password: str) -> Response:
        """Endpoint for authentication of user

        Args:
            email:    username
            password: password for username
        """
        data = {
            "email": email,
            "password": password,
        }
        path = self.url + "/authenticate"
        response = requests.post(url=path, data=json.dumps(data), headers=self.headers)
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

    def registration(self, body: dict) -> Response:
        """Endpoint for registration of user

        Args:
            body:   registration data with required fields:
                        email:      electronic mail;
                        firstName:  name;
                        lastName:   surname;
                        password:   password for electronic mail.
        """
        path = self.url + "/register"
        response = requests.post(url=path, data=json.dumps(body), headers=self.headers)
        log_request(response)

        return response
