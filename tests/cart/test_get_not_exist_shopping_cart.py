from allure import description, step, title, feature
from hamcrest import assert_that, is_

from framework.asserts.common import assert_response_message, assert_content_type
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI


@feature("Getting shopping  cart")
class TestCart:
    @title("Getting shopping cart that does not exist")
    @description(
        "GIVEN user is registered and does not have shopping cart"
        "WHEN user get the cart"
        "THEN status HTTP CODE = 404"
    )
    def test_get_user_cart(self, creating_user_via_api):
        token, user_id = creating_user_via_api

        with step("Get cart of user and verify that user doesn't have a shopping cart"):
            response_get_cart = CartAPI().get_user_cart(token=token, expected_status_code=404)

        with step("Checking response body and Content Type"):
            expected_message = f'The shopping cart for the user with id = {user_id} is not found.'
            assert_response_message(response_get_cart, expected_message)
            assert_content_type(response_get_cart, "application/json")

        with step("Deleting user"):
            UsersAPI().delete_user(token=token)
            response_after_del = UsersAPI().get_user(token=token)
            assert_that(response_after_del.status_code, is_(401))

