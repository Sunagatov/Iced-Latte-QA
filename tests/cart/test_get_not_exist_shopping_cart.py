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
        "THEN status HTTP CODE = 404 and the response body contains an appropriate error message."
    )
    def test_get_user_cart(self, create_and_delete_user_via_api):
        with step("Registration of user"):
            token, user_id = create_and_delete_user_via_api

        with step("Get cart of user and verify that user doesn't have a shopping cart"):
            response_get_cart = CartAPI().get_user_cart(token=token, expected_status_code=404)

        with step("Checking response body and Content Type"):
            expected_message = f'The shopping cart for the user with id = {user_id} is not found.'
            assert_response_message(response_get_cart, expected_message)
            assert_content_type(response_get_cart, "application/json")



