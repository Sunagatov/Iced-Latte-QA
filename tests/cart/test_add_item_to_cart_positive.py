from allure import description, step, title, feature
from hamcrest import assert_that, has_length, equal_to, has_key

from data.data_for_cart import data_for_adding_product_to_cart
from framework.asserts.common import assert_content_type
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.methods_to_cart import get_product_info, assert_product_to_add_matches_response


@feature("Adding items to cart ")
class TestCart:
    @title("Test add items to new user's cart")
    @description(
        "GIVEN user is registered and does not have any item in shopping cart"
        "WHEN user add the items to the cart"
        "THEN status HTTP CODE = 200 and response body  contains added item"
    )
    def test_add_item_to_cart(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Get user's info via API"):
            response_get_user_info = UsersAPI().get_user(token=token)
            new_user_id = response_get_user_info.json()["id"]

        with step("Get user's shopping cart and verify that user doesn't have items in shopping cart"):
            response_get_cart = CartAPI().get_user_cart(token=token)
            data = response_get_cart.json()
            assert_that(data, has_key("items"))
            assert_that(data["items"], has_length(0))

        with step("Add product to the shopping cart "):
            product_add_to_cart = data_for_adding_product_to_cart

            response_add_to_cart = CartAPI().add_item_to_cart(token=token,
                                                              items=product_add_to_cart)
            print(response_add_to_cart.json())

        with step("Verify product to add in response after API request"):
            product_list_in_response_add_to_cart = get_product_info(response=response_add_to_cart)
            assert_product_to_add_matches_response(product_add_to_cart, product_list_in_response_add_to_cart)

        with step("Verify the shopping cart created under new user/response body contain correct user's id)."):
            response_get_cart_after_add_product = CartAPI().get_user_cart(token=token)
            expected_user_id_in_cart = response_get_cart_after_add_product.json()["userId"]
            assert_that(new_user_id, equal_to(expected_user_id_in_cart), "Expected user ID does not match.")

        with step("Verify added products are in a shopping cart"):
            product_list_in_cart_after_add = get_product_info(response=response_get_cart_after_add_product)
            assert_product_to_add_matches_response(product_add_to_cart, product_list_in_cart_after_add)
            assert_content_type(response_get_cart, "application/json")
