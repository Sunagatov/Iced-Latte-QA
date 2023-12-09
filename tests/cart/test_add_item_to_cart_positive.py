from allure import description, step, title, feature
from hamcrest import assert_that, is_

from framework.asserts.common import assert_response_message, assert_content_type
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.methods_to_cart import assert_compare_product_to_add_with_response, \
    verify_products_in_response


@feature("Adding items to cart ")
class TestCart:
    @title("Test add items to new user's cart")
    @description(
        "GIVEN user is registered and does not have shopping cart"
        "WHEN user add the items to the cart"
        "THEN status HTTP CODE = 200"
        "And response body that contain added items returns"
    )
    def test_adding_item_to_cart(self, creating_user_via_api):
        token, new_user_id = creating_user_via_api

        with step("Get shopping cart of user and verify that user doesn't have a shopping cart"):
            response_get_cart = CartAPI().get_user_cart(token=token, expected_status_code=404)

        with step("Checking the response body and the Content-Type"):
            expected_message = f'The shopping cart for the user with id = {new_user_id} is not found.'
            assert_response_message(response_get_cart, expected_message)
            assert_content_type(response_get_cart, "application/json")

        with step("Generation data for adding to the shopping cart"):
            items_to_add = [
                {"productId": "ad0ef2b7-816b-4a11-b361-dfcbe705fc96", "productQuantity": 2},
                {"productId": "3ea8e601-24c9-49b1-8c65-8db8b3a5c7a3", "productQuantity": 3}
            ]

        with step("Adding new product to a shopping cart "):
            CartAPI().add_new_item_to_cart(token=token,
                                           items=items_to_add)

        with step("Checking: 1. The shopping cart created under new user. 2.Added products are in a shopping cart"):
            response_get_cart_after_add = CartAPI().get_user_cart(token=token)
            expected_user_id_in_cart = response_get_cart_after_add.json()["userId"]
            assert_that(expected_user_id_in_cart), is_(new_user_id)
            product_list_after_add = verify_products_in_response(response=response_get_cart_after_add)
            assert_compare_product_to_add_with_response(items_to_add, product_list_after_add)

        with step("Deleting user"):
            UsersAPI().delete_user(token=token)
            response_after_del = UsersAPI().get_user(token=token)
            expected_message_after_del_user = 'User with the provided email does not exist'
            assert_response_message(response_after_del, expected_message_after_del_user, )

