from allure import description, step, title, feature
from hamcrest import assert_that, is_

from configs import data_for_adding_product_to_cart
from framework.asserts.common import assert_response_message, assert_content_type
from framework.endpoints.cart_api import CartAPI
from framework.tools.methods_to_cart import assert_compare_product_to_add_with_response, \
    get_product_info


@feature("Adding items to cart ")
class TestCart:
    @title("Test add items to new user's cart")
    @description(
        "GIVEN user is registered and does not have shopping cart"
        "WHEN user add the items to the cart"
        "THEN status HTTP CODE = 200 and response body  contains added item"
    )
    def test_adding_item_to_cart(self, create_and_delete_user_via_api):
        with step("Registration of user"):
            token, new_user_id = create_and_delete_user_via_api

        with step("Get shopping cart of user and verify that user doesn't have a shopping cart"):
            response_get_cart = CartAPI().get_user_cart(token=token, expected_status_code=404)

        with step("Checking the response body and the Content-Type"):
            expected_message = f'The shopping cart for the user with id = {new_user_id} is not found.'
            assert_response_message(response_get_cart, expected_message)
            assert_content_type(response_get_cart, "application/json")

        with step("Generation data for adding to the shopping cart"):
            items_to_add = data_for_adding_product_to_cart

        with step("Adding new product to a shopping cart "):
            CartAPI().add_new_item_to_cart(token=token,
                                           items=items_to_add)

        with step("Checking: 1. The shopping cart created under new user. 2.Added products are in a shopping cart"):
            response_get_cart_after_add = CartAPI().get_user_cart(token=token)
            expected_user_id_in_cart = response_get_cart_after_add.json()["userId"]
            assert_that(expected_user_id_in_cart), is_(new_user_id)
            product_list_after_add = get_product_info(response=response_get_cart_after_add)
            assert_compare_product_to_add_with_response(items_to_add, product_list_after_add)
            assert_content_type(response_get_cart, "application/json")



