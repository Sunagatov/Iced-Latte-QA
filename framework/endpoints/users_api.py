import requests
from requests import Response

from configs import HOST


class UsersAPI:
    def __init__(self):
        self.url = HOST + "/api/v1/users"
        self.headers = {"Content-Type": "application/json"}

    def get_user_by_id(self, user_id: str, token: str) -> Response:
        """Getting info about user by id

        Args:
            user_id:    id of user;
            token:      JWT token for authorization of request
        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        url = self.url + "/{id}".format(id=user_id)
        response = requests.get(headers=headers, url=url)

        return response
