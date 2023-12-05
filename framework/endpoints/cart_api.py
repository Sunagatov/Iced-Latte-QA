import json
from hamcrest import assert_that, is_
import requests
from requests import Response

from configs import HOST

from framework.tools.logging import log_request


class CartAPI:
    def __init__(self):
        """Initializing parameters for request"""
        self.url = HOST + "/api/v1/cart"
        self.headers = {"Content-Type": "application/json"}

    def add_new_item_to_cart(self, token: str, id_product: str, quantity: int,
                             expected_status_code: int = 200) -> Response:
        """Endpoint for authentication of user

        Args:
            expected_status_code: expected http status code from response
            token: JWT token for authorization of request
            id_product: id product for adding to the cart
            quantity: quantity of product to adding to the cart

        """

        data = {
            "items": [
                {
                    "productId": id_product,
                    "productQuantity": quantity
                }
            ]
        }
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = self.url + "/items"
        response = requests.post(url=path, data=json.dumps(data), headers=headers)
        assert_that(response.status_code, is_(expected_status_code),
                    reason=f"Expected status code {expected_status_code}, found: {response.status_code}")
        log_request(response)

        return response

    def get_user_cart(self, token: str, expected_status_code: int = 200) -> Response:
        """

        Args:
            expected_status_code: expected http status code from response
            token: JWT token for authorization of request
        """
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = self.url
        response = requests.get(url=path, headers=headers)
        assert_that(response.status_code, is_(expected_status_code),
                    reason=f"Expected status code {expected_status_code}, found: {response.status_code}")
        log_request(response)

        return response

    # def update_item_in_cart_if_exists(self, token: str, product_id: str, quantity: int) -> Response:
    #     """
    #     Update the quantity of a product in the user's cart if it exists.
    #
    #     Args:
    #         token: JWT token for authorization of request.
    #         product_id: ID of the product to be updated in the cart.
    #         quantity: New quantity of the product.
    #     """
    #     self.headers["Authorization"] = f"Bearer {token}"
    #     response = self.get_user_cart(token)
    #     if response.status_code == 200:
    #         cart_items = response.json().get("items", [])
    #         if any(item['productInfo']['id'] == product_id for item in cart_items):
    #             data = {"productId": product_id, "productQuantity": quantity}
    #             path = f"{self.url}/items"
    #             update_response = requests.patch(url=path, data=json.dumps(data), headers=self.headers)
    #             log_request(update_response)
    #             return update_response
    #         else:
    #             return Response()  # or return a custom response indicating product is not in the cart
    #     return response  # return the response from get_user_cart if it's not 200
    def delete_item_from_cart(self, token: str, item_id: str, expected_status_code: int = 200) -> Response:
        """

        Args:
            item_id:
            expected_status_code: expected http status code from response
            token: JWT token for authorization of request
        """
        data = {
            "shoppingCartItemIds": [
                item_id
            ]
        }
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = self.url + "/items"
        response = requests.delete(url=path, data=json.dumps(data), headers=headers)
        assert_that(response.status_code, is_(expected_status_code),
                    reason=f"Expected status code {expected_status_code}, found: {response.status_code}")
        log_request(response)

        return response

    def update_quantity_product(self, token: str, item_id: str, quantity: int,
                                expected_status_code: int = 200) -> Response:
        """Endpoint for authentication of user

                Args:
                    expected_status_code: expected http status code from response
                    token: JWT token for authorization of request
                    item_id: product id to update
                    quantity: quantity of product to adding to the cart

                """

        data = {
            "shoppingCartItemId": item_id,
            "productQuantityChange": quantity
}
        headers = self.headers
        headers["Authorization"] = f"Bearer {token}"
        path = self.url + "/items"
        response = requests.patch(url=path, data=json.dumps(data), headers=headers)
        assert_that(response.status_code, is_(expected_status_code),
                    reason=f"Expected status code {expected_status_code}, found: {response.status_code}")
        log_request(response)

        return response
