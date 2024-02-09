from allure import description, step, title, feature
from hamcrest import assert_that, equal_to

from framework.endpoints.cart_api import CartAPI
from framework.tools.methods_to_cart import extract_random_item_detail, get_quantity_specific_cart_item


@feature("Updating item quantity in cart ")
class TestCart:
    @title("Test updating item quantity in new user's cart")
    @description(
        "GIVEN user is registered and have shopping cart"
        "WHEN user update item quantity in the shopping cart"
        "THEN status HTTP CODE = 200 and response body that contain updated 'productQuantity' returns"
    )
    def test_updating_increase_item_quantity_in_cart(self, creating_and_adding_product_to_shopping_cart):
        with step("Registration new user, and add product to the shopping cart"
                  "Getting info about user and user's shopping cart "):
            token, new_user_id, response_get_cart_after_added = creating_and_adding_product_to_shopping_cart

        with step("Getting random items to update from shopping cart and determination quantity for update "):
            random_item_from_cart = extract_random_item_detail(response_get_cart_after_added)
            item_id_to_update = random_item_from_cart["id"]
            item_quantity_before_update = random_item_from_cart["productQuantity"]
            quantity_to_update = 1

        with step("Update quantity of item"):
            response_after_update = CartAPI().update_quantity_product(token=token, item_id=item_id_to_update,
                                                                      item_quantity=quantity_to_update)

        with step("Verify that quantity of item is updated"):
            actual_item_quantity_after_update = get_quantity_specific_cart_item(response_after_update,
                                                                                item_id_to_update)
            expected_item_quantity_after_update = item_quantity_before_update + quantity_to_update
            assert_that(expected_item_quantity_after_update, equal_to(actual_item_quantity_after_update))

    def test_updating_decrease_item_quantity_in_cart(self, creating_and_adding_product_to_shopping_cart):
        with step("Registration new user, and add product to the shopping cart"
                  "Getting info about user and user's shopping cart "):
            token, new_user_id, response_get_cart_after_added = creating_and_adding_product_to_shopping_cart

        with step("Getting random items to update from shopping cart and determination quantity for update "):
            random_item_from_cart = extract_random_item_detail(response_get_cart_after_added)
            item_id_to_update = random_item_from_cart["id"]
            item_quantity_before_update = random_item_from_cart["productQuantity"]
            quantity_to_update = -1

        with step("Update quantity of item"):
            response_after_update = CartAPI().update_quantity_product(token=token, item_id=item_id_to_update,
                                                                      item_quantity=quantity_to_update)

        with step("Verify that quantity of item is updated"):
            actual_item_quantity_after_update = get_quantity_specific_cart_item(response_after_update,
                                                                                item_id_to_update)
            expected_item_quantity_after_update = item_quantity_before_update + quantity_to_update
            assert_that(expected_item_quantity_after_update, equal_to(actual_item_quantity_after_update))
