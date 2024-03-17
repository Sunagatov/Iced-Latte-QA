import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, has_length, has_key

from data.data_for_cart import id_product_not_exist_in_BD_for_adding_to_cart
from framework.asserts.assert_cart import assert_added_product_not_in_api_response
from framework.asserts.common import assert_content_type
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI


@feature("Adding item(product) to cart ")
class TestCart:
    @pytest.mark.critical
    @pytest.mark.skip(reason="BUG, user add product that not exist in BD, status code should be = 400, actual = 200")
    @title("Test add item(product) to new user's cart negative")
    @description(
        "GIVEN user is registered and does not have shopping cart"
        "WHEN user add the items that not exist in BD"
        "THEN status HTTP CODE = 400"
    )
    def test_adding_not_exist_item_to_cart(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Getting user's info via API"):
            getting_user_response = UsersAPI().get_user(token=token)
            new_user_id = getting_user_response.json()["id"]

        with step("Get user's shopping cart and verify that user doesn't have items in shopping cart"):
            response_get_cart = CartAPI().get_user_cart(token=token)
            data = response_get_cart.json()
            assert_that(data, has_key("items"))
            assert_that(data["items"], has_length(0))

        with step("Generating data to add to the shopping cart"):
            product_add_to_cart = id_product_not_exist_in_BD_for_adding_to_cart

        with step("Add not exist product to the shopping cart "):
            response_add_to_cart = CartAPI().add_item_to_cart(token=token,
                                                              items=product_add_to_cart, expected_status_code=400)

        with step("Verify,response does not contain not exist product."):
            assert_added_product_not_in_api_response(response_add_to_cart, product_add_to_cart)

        with step("Verify,not exist product was not added to the cart."):
            response_get_cart_after_add = CartAPI().get_user_cart(token=token)
            assert_added_product_not_in_api_response(response_get_cart_after_add, product_add_to_cart)
            assert_content_type(response_get_cart, "application/json")

