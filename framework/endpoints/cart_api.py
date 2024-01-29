import json
from hamcrest import assert_that, is_
import requests
from requests import Response

from configs import HOST
from framework.asserts.common import assert_status_code

from framework.tools.logging_allure import log_request


class CartAPI:
    def __init__(self):
        """Initializing parameters for request"""
        self.url = HOST + "/api/v1/cart"
        self.headers = {"Content-Type": "application/json"}

    def get_user_cart(self, token: str, expected_status_code: int = 200) -> Response:
        """ Getting info about user's shopping cart

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

    def update_quantity_product(self, token: str, item_id: str, item_quantity: int,
                                expected_status_code: int = 200) -> Response:
        """Updating product's quantity

        Args:
            item_quantity: quantity to update
            item_id: item to update
            expected_status_code: expected http status code from response
            token: JWT token for authorization of request
        """
        body = {"shoppingCartItemId": item_id,
                "productQuantityChange": item_quantity
                }
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = self.url + "/items"
        response = requests.patch(url=path, data=json.dumps(body), headers=headers)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)
        return response

    def add_new_item_to_cart(self, token: str, items: list, expected_status_code: int = 200) -> Response:
        """Adding multiple products to cart and verifying if they are in the response

        Args:
            items: A list of items where each item is a dictionary containing 'productId' and 'productQuantity'
            expected_status_code (int): Expected HTTP status code from response
            token (str): JWT token for authorization of request

        Example:
            items = [
                {"productId": "123ffg-333-jjj78", "productQuantity": 2},
                {"productId": "6788gg-uh8-hajj6", "productQuantity": 3}
            ]
        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = self.url + "/items"
        body = {"items": items}
        response = requests.post(url=path, data=json.dumps(body), headers=headers)
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)
        return response

    def delete_item_from_cart(self, token: str, cart_item_id: list, expected_status_code: int = 200) -> Response:
        """Deleting item from shopping cart

        Args:
            cart_item_id:  data for deleting items from shopping cart with required fields
            expected_status_code: expected http status code from response
            token: JWT token for authorization of request
        """

        body = {
            "shoppingCartItemIds": cart_item_id

        }
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = self.url + "/items"
        response = requests.delete(url=path, headers=headers, data=json.dumps(body))
        assert_status_code(response, expected_status_code=expected_status_code)
        log_request(response)

        return response
