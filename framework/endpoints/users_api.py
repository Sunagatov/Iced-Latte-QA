import json
import os
from pathlib import Path

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

    def change_password(self, token: str, new_password: str, old_password: str,
                        expected_status_code: int = 200) -> Response:
        """ Change user password

        Args:
            old_password: old password
            new_password: new password
            expected_status_code: Expected HTTP code from Response
            token: JWT token for authorization of request

        """
        data = {
            "newPassword": new_password,
            "oldPassword": old_password
        }
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        response = requests.patch(headers=headers, url=self.url, data=json.dumps(data))
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response

    def get_user_avatar(self, token: str = "", expected_status_code: int = 200) -> Response:
        """Getting info about user's avatar via API

        Args:
            expected_status_code: Expected HTTP code from Response
            token:      JWT token for authorization of request
        """
        headers = self.headers
        path = f"{self.url}/avatar"
        headers["Authorization"] = f"Bearer {token}"
        response = requests.get(headers=headers, url=path)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response

    def post_user_avatar(self, token: str, image_path: str, expected_status_code: int = 200) -> Response:
        """Posts a user's avatar image to the API

         Args:
            token: JWT token for authorization of the request
            image_path: Path to the image file to be uploaded
            expected_status_code: Expected HTTP status code from the response
        """
        headers = self.headers
        path = f"{self.url}/avatar"
        headers["Authorization"] = f"Bearer {token}"

        # Open the image file in binary mode
        with open(image_path, 'rb') as image_file:

            files = {"file": (os.path.basename(image_path), image_file, 'multipart/form-data')}
            response = requests.post(url=path, headers=headers, files=files)

        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)  # Make sure you have a function to log the request and response details

        return response

