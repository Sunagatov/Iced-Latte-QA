from allure import description, step, title, feature

from framework.asserts.assert_cart import assert_deleted_item_ids_in_response
from framework.asserts.common import assert_content_type
from framework.endpoints.cart_api import CartAPI
from framework.tools.methods_to_cart import get_item_id


@feature("Deleting item/items from cart ")
class TestCart:
    @title("Test deleting ALL items from new user's cart")
    @description(
        "GIVEN user is registered and  has shopping cart"
        "WHEN user delete ALL items from  cart"
        "THEN status HTTP CODE = 200"
    )
    def test_deleting_items_from_cart(self, creating_and_adding_product_to_shopping_cart):
        with step("Registration new user, and add product to the shopping cart"
                  "Getting info about user and user's shopping cart "):
            token, new_user_id, response_get_cart_after_added = creating_and_adding_product_to_shopping_cart

        with step("Generating data for delete"):
            item_to_delete_more_than_one = get_item_id(response_get_cart_after_added)
            response_delete_item = CartAPI().delete_item_from_cart(token=token,
                                                                   cart_item_id=item_to_delete_more_than_one)

        with step("Checking the response and Content-Type"):
            assert_content_type(response_delete_item, "application/json")

        with step("Verify that deleted items do not exist in shopping cart"):
            assert_deleted_item_ids_in_response(response_delete_item, item_to_delete_more_than_one)

    @title("Test deleting item from new user's cart")
    @description(
        "GIVEN user is registered and does not have shopping cart"
        "WHEN user delete item from the cart"
        "THEN status HTTP CODE = 200"
    )
    def test_deleting_one_item_from_cart(self, creating_and_adding_product_to_shopping_cart):
        with step("Registration new user, and add product to the shopping cart"
                  "Getting info about user and user's shopping cart "):
            token, new_user_id, response_get_cart_after_added = creating_and_adding_product_to_shopping_cart

        with step("Generating data for delete one product from cart"):
            id_one_item_to_delete = [response_get_cart_after_added.json()["items"][0]["id"]]
            print(id_one_item_to_delete)
            id_one_item_to_delete1 = id_one_item_to_delete

        with step("Deleting item from cart"):
            response_delete_item = CartAPI().delete_item_from_cart(token=token,
                                                                   cart_item_id=id_one_item_to_delete)
            assert_content_type(response_delete_item, "application/json")

        with step("Verify that deleted items do not exist in shopping cart"):
            assert_deleted_item_ids_in_response(response_delete_item, id_one_item_to_delete1)
