from allure import description, step, title, feature
from hamcrest import assert_that, has_key, has_length, equal_to

from configs import data_for_not_exist_shopping_cart_item_id
from framework.asserts.common import assert_response_message, assert_content_type
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.methods_to_cart import extract_random_item_detail, get_quantity_specific_cart_item


@feature("Updating  item's quantity negative")
class TestCart:
    @title("Updating  item's quantity negative")
    @description(
        "GIVEN user is registered and has items shopping cart"
        "WHEN user try to decrease  item's quantity that > than actual item quantity in shopping cart"
        "THEN status HTTP CODE = 400 and response body that contain appropriate error message returns"
    )
    def test_updating_decrease_item_quantity_in_cart(self, creating_and_adding_product_to_shopping_cart):
        with step("Registration new user, and add product to the shopping cart"
                  "Getting info about user and user's shopping cart "):
            token, new_user_id, response_get_cart_after_added = creating_and_adding_product_to_shopping_cart

        with step("Getting random items to update from shopping cart and determination quantity for update "):
            random_item_from_cart = extract_random_item_detail(response_get_cart_after_added)
            item_id_to_update = random_item_from_cart["id"]
            item_quantity_before_update = random_item_from_cart["productQuantity"]
            quantity_to_update = -5

        with step("Update quantity of item"):
            response_after_update = CartAPI().update_quantity_product(token=token, item_id=item_id_to_update,
                                                                      item_quantity=quantity_to_update,
                                                                      expected_status_code=400)

        with step("Verify the error message from request for update"):
            expected_message = f"Invalid product quantity = {item_quantity_before_update + quantity_to_update} or product quantity without changes"
            assert_response_message(response_after_update, expected_message=expected_message)

        with step("Get shopping cart of user and verify that quantity is not updated"):
            response_get_cart = CartAPI().get_user_cart(token=token)
            actual_item_in_cart = get_quantity_specific_cart_item(response_get_cart,
                                                                  item_id_to_update)
            assert_that(item_quantity_before_update, equal_to(actual_item_in_cart))

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
            shopping_cart_item_id = data_for_update_not_exist_item["shoppingCartItemId"]
            response_after_update = CartAPI().update_quantity_product(token=token,
                                                                      item_id=data_for_update_not_exist_item[
                                                                          "shoppingCartItemId"],
                                                                      item_quantity=data_for_update_not_exist_item[
                                                                          "productQuantityChange"],
                                                                      expected_status_code=404)

        with step("Checking the response body and the Content-Type"):
            expected_message_after_update = f"The shopping cart item with shoppingCartItemId = {shopping_cart_item_id} is not found."
            assert_response_message(response_after_update, expected_message_after_update)
            assert_content_type(response_after_update, "application/json")

