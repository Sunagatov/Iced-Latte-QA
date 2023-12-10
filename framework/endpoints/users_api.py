import requests
from hamcrest import assert_that, is_
from requests import Response

from configs import HOST
from framework.tools.logging import log_request


class UsersAPI:
    def __init__(self):
        self.url = HOST + "/api/v1/users"
        self.headers = {"Content-Type": "application/json"}

    def get_user(self, token: str = "") -> Response:
        """Getting info about user

        Args:
            token:      JWT token for authorization of request
        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        response = requests.get(headers=headers, url=self.url)
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
        assert_that(response.status_code, is_(expected_status_code),
                    reason=f"Expected status code {expected_status_code}, found: {response.status_code}")
        log_request(response)
        return response
