from allure import description, step, title, feature
from hamcrest import assert_that, has_length, equal_to, has_key


from configs import data_for_adding_product_to_cart
from framework.asserts.common import assert_response_message, assert_content_type
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI
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
    def test_adding_item_to_cart(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Getting user's info via API"):
            getting_user_response = UsersAPI().get_user(token=token)
            new_user_id = getting_user_response.json()["id"]

        with step("Get shopping cart of user and verify that user doesn't have items in shopping cart"):
            response_get_cart = CartAPI().get_user_cart(token=token)
            data = response_get_cart.json()
            assert_that(data, has_key("items"))
            assert_that(data["items"], has_length(0))

        with step("Verify content-type"):
            assert_content_type(response_get_cart, "application/json")

        with step("Generation data for adding to the shopping cart"):
            items_to_add = data_for_adding_product_to_cart

        with step("Adding new product to a shopping cart "):
            CartAPI().add_new_item_to_cart(token=token,
                                           items=items_to_add)

        with step("Checking: 1. The shopping cart created under new user. 2.Added products are in a shopping cart"):
            response_get_cart_after_add = CartAPI().get_user_cart(token=token)
            expected_user_id_in_cart = response_get_cart_after_add.json()["userId"]
            assert_that(new_user_id, equal_to(expected_user_id_in_cart), "Expected user ID does not match.")
            product_list_after_add = get_product_info(response=response_get_cart_after_add)
            assert_compare_product_to_add_with_response(items_to_add, product_list_after_add)
            assert_content_type(response_get_cart, "application/json")
