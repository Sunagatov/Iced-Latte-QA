import requests
from requests import Response

from configs import HOST


class ProductAPI:
    def __init__(self):
        self.url = HOST + "/api/v1/products"
        self.headers = {"Content-Type": "application/json"}

    def get_by_id(self, _id: str, token: str = None) -> Response:
        """Getting product info by id

        Args:
            token:  JWT token for authorization of request;
            _id:    product ID.
        """
        headers = self.headers
        if token:
            headers["Authorization"] = f"Bearer {token}"
        url = self.url + f"/{_id}"
        response = requests.get(headers=headers, url=url)
        return response

    def get_all(self, token: str = None, params: dict = None) -> Response:
        """Getting info about all products

        Args:
            token:  JWT token for authorization of request;
            params: URL-parameters request.
        """
        headers = self.headers
        if token:
            headers["Authorization"] = f"Bearer {token}"
        response = requests.get(headers=headers, url=self.url, params=params)
        return response
