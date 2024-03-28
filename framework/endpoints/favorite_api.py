import json
from typing import Optional, Union

import requests
from requests import Response

from configs import HOST
from framework.asserts.common import assert_status_code, assert_content_type
from framework.tools.logging_allure import log_request


class FavoriteAPI:
    def __init__(self):
        """Initializing parameters for request"""
        self.url = HOST + "/api/v1/favorites"
        self.headers = {"Content-Type": "application/json"}

    def add_favorites(
        self, token: str, favorite_product: list[str], expected_status_code: int = 200
    ) -> Response:
        """Add product to favorites

        Args:
            favorite_product: list product/products to add to favorites
            expected_status_code: expected http status code from response
            token: JWT token for authorization of request
        """
        data = {"productIds": favorite_product}

        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = self.url
        response = requests.post(url=path, data=json.dumps(data), headers=headers)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response

    def get_favorites(self, token: str, expected_status_code: int = 200) -> Response:
        """Getting info about user's shopping cart

        Args:
            expected_status_code: expected http status code from response
            token: JWT token for authorization of request
        """

        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = self.url
        response = requests.get(url=path, headers=headers)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response

    def delete_favorites(
        self, token: str, id_product: str, expected_status_code: int = 200
    ) -> Response:
        """Add product to favorites

        Args:
            id_product: product to delete from favorite list
            expected_status_code: expected http status code from response
            token: JWT token for authorization of request
        """

        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = f"{self.url}/{id_product}"
        response = requests.delete(url=path, headers=headers)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response
