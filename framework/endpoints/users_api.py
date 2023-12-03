import requests
from requests import Response

from configs import HOST
from framework.tools.logging import log_request


class UsersAPI:
    def __init__(self):
        self.url = HOST + "/api/v1/users"
        self.headers = {"Content-Type": "application/json"}

    def get_user(self, token: str = "") -> Response:
        """Getting info about user via API

        Args:
            token:      JWT token for authorization of request
        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        response = requests.get(headers=headers, url=self.url)
        log_request(response)

        return response

    def update_user(self, token: str = "", user_data: dict = None) -> Response:
        """Updating user info

        Args:
            token:      JWT token for authorization of request
            user_data:  data for updating user info
        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        response = requests.put(headers=headers, url=self.url, json=user_data)
        log_request(response)

        return response
