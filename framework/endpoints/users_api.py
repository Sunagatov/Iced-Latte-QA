import requests
from requests import Response

from configs import HOST
from framework.tools.logging import log_request


class UsersAPI:
    def __init__(self):
        self.url = HOST + "/api/v1/users"
        self.headers = {"Content-Type": "application/json"}

    def get_user_by_id(self, token: str = "") -> Response:
        """Getting info about user by id

        Args:
            token:      JWT token for authorization of request
        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        response = requests.get(headers=headers, url=self.url)
        log_request(response)

        return response
