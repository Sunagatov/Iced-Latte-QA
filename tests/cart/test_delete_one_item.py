from allure import description, step, title, feature
from hamcrest import assert_that, has_key, has_length, equal_to


from configs import data_for_adding_product_to_cart
from framework.asserts.common import assert_response_message, assert_content_type
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.methods_to_cart import get_product_info, \
    assert_compare_product_to_add_with_response


@feature("Deleting item from cart ")
class TestCart:
    @title("Test deleting item from new user's cart")
    @description(
        "GIVEN user is registered and does not have shopping cart"
        "WHEN user delete item from the cart"
        "THEN status HTTP CODE = 200"
    )
    def test_deleting_item_from_cart(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Getting user's info via API"):
            getting_user_response = UsersAPI().get_user(token=token)
            new_user_id = getting_user_response.json()["id"]

        with step("Getting shopping cart of user"):
            response_get_cart = CartAPI().get_user_cart(token=token)

        with step("Verify user doesn't have items in shopping cart"):
            data = response_get_cart.json()
            assert_that(data, has_key("items"))
            assert_that(data["items"], has_length(0))

        with step("Adding new products to a shopping cart "):
            CartAPI().add_new_item_to_cart(token=token,
                                           items=data_for_adding_product_to_cart)

        with step("Verify: 1. The shopping cart created under new user. 2.added products are in a shopping cart"):
            response_get_cart_after_add = CartAPI().get_user_cart(token=token)
            expected_user_id_in_cart = response_get_cart_after_add.json()["userId"]
            assert_that(new_user_id, equal_to(expected_user_id_in_cart), "Expected user ID does not match.")
            product_list_after_add = get_product_info(response=response_get_cart_after_add)
            assert_compare_product_to_add_with_response(data_for_adding_product_to_cart, product_list_after_add)

        with step("Generating data for delete"):
            cart_id_one_item = [response_get_cart_after_add.json()["items"][0]["id"]]

        with step("Deleting item from cart"):
            response_delete_item = CartAPI().delete_item_from_cart(token=token,
                                                                   cart_item_id=cart_id_one_item)
            assert_content_type(response_delete_item, "application/json")
