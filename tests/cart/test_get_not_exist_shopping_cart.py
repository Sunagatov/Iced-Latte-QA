from allure import description, step, title, feature
from hamcrest import assert_that, has_key, has_length

from framework.asserts.common import assert_response_message, assert_content_type
from framework.endpoints.cart_api import CartAPI


@feature("Getting shopping  cart")
class TestCart:
    @title("Getting shopping cart that does not exist")
    @description(
        "GIVEN user is registered and does not have shopping cart"
        "WHEN user get the cart"
        "THEN status HTTP CODE = 200 and the response body contains response items=[]/empty."
    )
    def test_get_user_cart(self, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Get not exist user's shopping cart"):
            response_get_cart = CartAPI().get_user_cart(token=token, expected_status_code=200)

        with step("Verify content-type and user doesn't have items in shopping cart"):
            data = response_get_cart.json()
            assert_that(data, has_key("items"))
            assert_that(data["items"], has_length(0))
            assert_content_type(response_get_cart, "application/json")
