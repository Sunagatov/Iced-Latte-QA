import json
from typing import Optional

import requests
from requests import Response

from configs import HOST


class AuthenticateAPI:
    def __init__(self):
        """Initializing parameters for request"""
        self.url = HOST + "/api/v1/auth"
        self.headers = {"Content-Type": "application/json"}

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

        return response
