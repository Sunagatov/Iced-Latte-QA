import requests
from requests import Response

from configs import HOST
from framework.asserts.common import assert_status_code
from framework.tools.logging_allure import log_request


class UsersAPI:
    def __init__(self):
        self.url = HOST + "/api/v1/users"
        self.headers = {"Content-Type": "application/json"}

    def get_user(self, token: str = "", expected_status_code: int = 200) -> Response:
        """Getting info about user via API

        Args:
            expected_status_code: Expected HTTP code from Response
            token:      JWT token for authorization of request
        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        response = requests.get(headers=headers, url=self.url)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response

    def delete_user(self, token: str, expected_status_code: int = 200) -> Response:
        """ Deleting user

        Args:
            expected_status_code: Expected HTTP code from Response
            token: JWT token for authorization of request

        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        response = requests.delete(headers=headers, url=self.url)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

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
