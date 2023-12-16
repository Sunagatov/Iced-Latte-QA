from allure import description, step, title, feature

from configs import data_for_not_exist_shopping_cart_item_id
from framework.asserts.common import assert_response_message, assert_content_type
from framework.endpoints.cart_api import CartAPI


@feature("Updating NOT existing item's quantity in cart ")
class TestCart:
    @title("Test updating NOT existing item quantity in user's shopping cart")
    @description(
        "GIVEN user is registered and have shopping cart"
        "WHEN user try to update not exist item's quantity in the shopping cart"
        "THEN status HTTP CODE = 404 and response body that contain appropriate error message returns"
    )
    def test_updating_not_exist_item_in_cart(self, creating_and_adding_product_to_shopping_cart):
        with step("Registration new user, and add product to the shopping cart"
                  "Getting info about user and user's shopping cart "):
            token, new_user_id, response_get_cart_after_added = creating_and_adding_product_to_shopping_cart

        with step("Update quantity of product"):
            data_for_update_not_exist_item = data_for_not_exist_shopping_cart_item_id
            response_after_update = CartAPI().update_quantity_product(token=token,
                                                                      item_id=data_for_update_not_exist_item[
                                                                          "shoppingCartItemId"],
                                                                      item_quantity=data_for_update_not_exist_item[
                                                                          "productQuantityChange"],
                                                                      expected_status_code=404)

        with step("Checking the response body and the Content-Type"):
            expected_message_after_update = "The shopping cart item with shoppingCartItemId = ec39b8c6-ba83-4f0a-8332-0769be35d5f9 is not found."
            assert_response_message(response_after_update, expected_message_after_update)
            assert_content_type(response_after_update, "application/json")


