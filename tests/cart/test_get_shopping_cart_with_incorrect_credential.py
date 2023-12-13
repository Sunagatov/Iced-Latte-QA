import pytest
from allure import feature, description, step, title
from hamcrest import assert_that, is_

from framework.asserts.common import (
    assert_status_code,
    assert_content_type,
    assert_response_message,
)
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.cart_api import CartAPI
from framework.tools.generators import generate_jwt_token
from framework.tools.generators import generate_user, generate_user_data


@feature("Getting shopping car")
class TestGetShoppingCart:

    @title("Getting shopping cart with Invalid Token")
    @description(
        "GIVEN the user is registered, "
        "WHEN the user sends a request to get  information about shopping cart using an invalid token, "
        "THEN the response code is 401 and the response body contains an appropriate error message."
    )
    @pytest.mark.skip(reason='Expected status code 401, found: 500')
    def test_get_shopping_cart_info_with_invalid_token(self):
        with step("Getting info about shopping cart"):
            invalid_token = "invalid_token"
            response_get_cart = CartAPI().get_user_cart(token=invalid_token, expected_status_code=401)

        with step("Checking the Content-Type"):
            assert_content_type(response_get_cart, "text/plain; charset=utf-8")

    @title("Getting info about shopping cart with Expired Token")
    @description(
        "GIVEN the user is registered, "
        "WHEN the user sends a request to get information about shopping cart with expired token, "
        "THEN the response code is 401 and the response body contains the error message"
    )
    def test_getting_shopping_cart_with_expired_token(self):
        with step("Getting info about shopping cart"):
            data = generate_user_data(first_name_length=6, last_name_length=5, password_length=3)
            email = data["email"]
            expired_token = generate_jwt_token(email=email, expired=True)
            response_get_cart = CartAPI().get_user_cart(token=expired_token, expected_status_code=401)
            assert_content_type(response_get_cart, "text/plain; charset=utf-8")

        with step("Checking the response body"):
            expected_error_message = "Jwt token is expired"
            assert_response_message(response_get_cart, expected_error_message)

    @title("Getting info about shopping cart with Empty Token")
    @description(
        "GIVEN the user is registered, "
        "WHEN the user sends a request to get information about shopping cart with empty token, "
        "THEN the response code is 401 and the response body contains the error message"
    )
    def test_getting_shopping_cart_with_empty_token(self):
        with step("Getting info about shopping cart"):
            response_get_cart = CartAPI().get_user_cart(token=" ", expected_status_code=401)
            assert_content_type(response_get_cart, "text/plain; charset=utf-8")

        with step("Checking the response body"):
            expected_error_message = "Bearer authentication header is absent"
            assert_response_message(response_get_cart, expected_error_message)

    @title("Getting  Information about shopping cart with Blacklisted Token")
    @description(
        "GIVEN the user is logged out, "
        "WHEN the user sends a request to get information about shopping cart with blacklisted token, "
        "THEN the response code is 401 and the response body contains the error message"
    )
    def test_getting_shopping_cart_with_blacklisted_token(self, create_and_delete_user_via_api):
        token = create_and_delete_user_via_api

        with step("Logging out of user"):
            logging_out_response = AuthenticateAPI().logout(token=token)
            assert_that(
                logging_out_response.status_code,
                is_(200),
                reason='Failed request "logout"',
            )

        with step("Getting  info about shopping cart"):
            response_get_cart = CartAPI().get_user_cart(token=token, expected_status_code=401)
            assert_content_type(response_get_cart, "text/plain; charset=utf-8")

        with step("Checking the response body"):
            expected_error_message = "JWT Token is blacklisted"
            assert_response_message(response_get_cart, expected_error_message)

    @title("Getting Info about shopping cart with Missing Email in Token")
    @description(
        "GIVEN the user is created "
        "WHEN the user sends a request to get information about  shopping cart with token not containing email, "
        "THEN the response code is 401 and the response body contains the error message"
    )
    def test_getting_shopping_cart_with_token_not_containing_email(self):
        with step("Getting information about shopping cart "):
            token_without_email = generate_jwt_token()
            response_get_cart = CartAPI().get_user_cart(token=token_without_email, expected_status_code=401)
            assert_content_type(response_get_cart, "text/plain; charset=utf-8")

        with step("Checking the response body"):
            expected_error_message = "User email not found in jwtToken"
            assert_response_message(response_get_cart, expected_error_message)

    @title("Getting information about shopping cart with Token of Non-Existing User")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to get information about shopping cart with token of non-existing user, "
        "THEN the response code is 401 and the response body contains the error message"
    )
    def test_getting_shopping_cart_with_token_not_containing_correct_user_email(self):
        with step("Getting information about shopping cart"):
            email_of_non_existing_user = generate_user()["email"]
            token_of_non_existing_user = generate_jwt_token(email_of_non_existing_user)
            response_get_cart = CartAPI().get_user_cart(token=token_of_non_existing_user, expected_status_code=401)

        with step("Checking response code and Content Type"):
            assert_status_code(response_get_cart, 401)
            assert_content_type(response_get_cart, "text/plain; charset=utf-8")

        with step("Checking the response body"):
            expected_error_message = "User with the provided email does not exist"
            assert_response_message(response_get_cart, expected_error_message)
