from allure import description, step, title, feature
from hamcrest import assert_that, has_key, has_length, equal_to

from framework.asserts.common import assert_response_message, assert_content_type
from framework.endpoints.cart_api import CartAPI
from framework.endpoints.users_api import UsersAPI


@feature("Get shopping  cart")
class TestCart:
    @title("Get shopping cart with no item in it ")
    @description(
        "GIVEN user is registered and does not have shopping cart"
        "WHEN user get the cart"
        "THEN status HTTP CODE = 200 and the response body contains response items=[]/empty."
    )
    def test_get_user_cart(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Get user's id info."):
            response_get_user_info = UsersAPI().get_user(token=token)
            new_user_id = response_get_user_info.json()["id"]

        with step("Get user's shopping cart. "):
            response_get_cart = CartAPI().get_user_cart(token=token, expected_status_code=200)

        with step("Verify user's ID in the shopping cart/response body contain correct user's id."):
            expected_user_id_in_cart = response_get_cart.json()["userId"]
            assert_that(new_user_id, equal_to(expected_user_id_in_cart), "Expected user ID does not match.")

        with step("Verify that user doesn't have items in shopping cart"):
            data = response_get_cart.json()
            assert_that(data, has_key("items"))
            assert_that(data["items"], has_length(0))

        with step("Verify content-type."):
            assert_content_type(response_get_cart, "application/json")
