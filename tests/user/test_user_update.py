from allure import feature, description, step, title
from hamcrest import assert_that, is_

from framework.asserts.common import (
    assert_status_code,
    assert_content_type,
    assert_response_message,
)
from framework.asserts.user_asserts import assert_update_user_data_matches
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import generate_user, generate_user_with_address


@feature("Update user's information")
class TestUpdateUser:
    @title("Updating User's Own Information")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to update their own information, "
        "THEN the response code is 200 and the response body contains the current user's data."
    )
    def test_update_user_info(self, create_authorized_user):
        token = create_authorized_user["token"]

        with step("Generating new user data"):
            user_data_to_update = generate_user()

        with step("Updating user info via API"):
            updating_user_response = UsersAPI().update_user(
                token=token, user_data=user_data_to_update
            )

        with step("Checking the response code"):
            assert_status_code(updating_user_response, 200)

        with step("Checking the response type of the body"):
            assert_content_type(updating_user_response, "application/json")

        with step("Checking the response "):
            assert_update_user_data_matches(
                updating_user_response.json(), user_data_to_update
            )

    @title("Updating User's Email is ignored")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to update their own email, "
        "THEN the response code is 200 and the response body contains the current user's email."
    )
    def test_update_user_email(self, create_authorized_user):
        token = create_authorized_user["token"]

        with step("Generating new user data"):
            user_data_to_update = generate_user()

        with step("Updating user info via API"):
            updating_user_response = UsersAPI().update_user(
                token=token, user_data=user_data_to_update
            )

        with step("Checking the response code"):
            assert_status_code(updating_user_response, 200)

        with step("Checking the response type of the body"):
            assert_content_type(updating_user_response, "application/json")

        with step("Checking the response "):
            response = updating_user_response.json()
            assert_that(response["email"], is_(create_authorized_user["user"]["email"]))

    @title("Updating User's Own Address")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to update their own address, "
        "THEN the response code is 200 and the response body contains the current user's address."
    )
    def test_update_user_address(self, create_authorized_user):
        token = create_authorized_user["token"]

        with step("Generating new user data"):
            user_data_to_update = generate_user_with_address()
            print(user_data_to_update)

        with step("Updating user info via API"):
            updating_user_response = UsersAPI().update_user(
                token=token, user_data=user_data_to_update
            )

        with step("Checking the response code"):
            assert_status_code(updating_user_response, 200)

        with step("Checking the response type of the body"):
            assert_content_type(updating_user_response, "application/json")

        with step("Checking the response "):
            print(updating_user_response.json()["address"])
            print(user_data_to_update["address"])
            assert_that(
                updating_user_response.json()["address"],
                is_(user_data_to_update["address"]),
            )
