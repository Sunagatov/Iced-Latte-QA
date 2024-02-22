from allure import feature, description, step, title
from hamcrest import assert_that, is_

from framework.asserts.common import (
    assert_status_code,
    assert_content_type,
    assert_response_message, assert_message_in_response,
)
from framework.asserts.user_asserts import assert_update_user_data_matches
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import generate_user
import pytest


@feature("Update user's information")
class TestUpdateUser:
    @pytest.mark.skip(reason="Email is not updated after request. link to bug - "
                             "https://trello.com/c/WB6FZG8a/4-%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5-email-%D0%BD%D0%B5-%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82")
    @title("Updating User Information")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to update their own information - email  "
        "THEN the response code is 200 and the response body contains the current user's data."
    )
    def test_update_user_email(self, create_authorized_user):
        token, user = create_authorized_user["token"], create_authorized_user["user"]

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

    @title("Updating User's Own Address")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to update their own address, "
        "THEN the response code is 200 and the response body contains the current user's address."
    )
    def test_update_user_address(self, create_authorized_user):
        token = create_authorized_user["token"]

        with step("Generating new user data"):
            user_data_to_update = generate_user(with_address=True)

        with step("Updating user info via API"):
            updating_user_response = UsersAPI().update_user(
                token=token, user_data=user_data_to_update
            )

        with step("Checking the response code"):
            assert_status_code(updating_user_response, 200)

        with step("Checking the response type of the body"):
            assert_content_type(updating_user_response, "application/json")

        with step("Checking the response "):
            assert_that(
                updating_user_response.json()["address"],
                is_(user_data_to_update["address"]),
            )

    @pytest.mark.parametrize(
        "first_name, last_name",
        [("John", "Doe"), ("Anne-Marie", "O'Conner"), ("O'Brien", "Smith-Jones"), ("Brien", "Smith Jones"),
         ("Smith Jones", "Smith")],
    )
    def test_update_user_with_valid_names(
            self, create_authorized_user, first_name, last_name
    ):
        token = create_authorized_user["token"]

        with step("Generating new user data"):
            # Include the last_name in the user data generation
            user_data_to_update = generate_user(
                firstName=first_name, lastName=last_name, email=create_authorized_user["user"]["email"]
            )

        with step("Updating user info via API"):
            updating_user_response = UsersAPI().update_user(
                token=token, user_data=user_data_to_update
            )

        with step("Checking the response type of the body"):
            assert_content_type(updating_user_response, "application/json")

        with step("Checking the response code"):
            assert_status_code(updating_user_response, 200)

        with step("Checking the response"):
            # Ensure that both first and last name are correctly updated
            assert_update_user_data_matches(
                updating_user_response.json(), user_data_to_update
            )

    @pytest.mark.skip(
        reason="Fields First Name and Last Name are not updated with valid length. link to bug - https://trello.com/c/0bWwMrXS/9-first-name-and-last-name-do-not-accept-length-55")
    @pytest.mark.parametrize(
        "first_name_length, last_name_length",
        [
            pytest.param(
                2,
                2,
            ),
            pytest.param(
                3,
                3,
            ),
            pytest.param(
                64,
                64,
            ),
            pytest.param(
                128,
                128,
            ),
            pytest.param(
                127,
                127,
            ),
        ],

    )
    def test_update_user_first_name_with_valid_length(
            self,
            create_authorized_user,
            first_name_length,
            last_name_length,

    ):
        token = create_authorized_user["token"]

        with step("Generating new user data"):
            user_data_to_update = generate_user(
                first_name_length=first_name_length, last_name_length=last_name_length
            )

        with step("Updating user info via API"):
            updating_user_response = UsersAPI().update_user(
                token=token, user_data=user_data_to_update
            )

        with step("Checking the response code"):
            assert_status_code(updating_user_response, 200)

        with step("Checking the response type of the body"):
            assert_content_type(updating_user_response, "application/json")

    @pytest.mark.parametrize(
        "first_name, last_name, expected_message",
        [
            pytest.param(
                None,
                "Doe",
                "First name is the mandatory attribute",
                marks=pytest.mark.xfail(
                    reason="BUG: IL-231: Absence of 'First Name is Mandatory' validation error on user data update"
                ),
            ),
            pytest.param(
                "John",
                None,
                "Last name is the mandatory attribute",
                marks=pytest.mark.xfail(
                    reason="BUG: IL-250: Absence of 'Last Name is Mandatory' validation error on user data update"
                ),
            ),
            pytest.param(
                "John123",
                "Doe",
                "First name can only contain letters",
                marks=pytest.mark.xfail(
                    reason="BUG: IL-240: API Update User - First Name and Last Name Allows Non-Latin Characters, Contrary to Requirements"
                ),
            ),
            pytest.param(
                "John",
                "Smith123",
                "Last name can only contain letters",
                marks=pytest.mark.xfail(
                    reason="BUG: IL-240: API Update User - First Name and Last Name Allows Non-Latin Characters, Contrary to Requirements"
                ),
            ),
        ],
    )
    def test_update_user_with_invalid_first_name_and_last_name(
            self, create_authorized_user, first_name, last_name, expected_message
    ):
        token = create_authorized_user["token"]

        with step("Generating new user data"):
            user_data_to_update = generate_user(
                firstName=first_name, last_name=last_name
            )
            if first_name is None:
                user_data_to_update.pop("firstName")

        with step("Updating user info via API"):
            updating_user_response = UsersAPI().update_user(
                token=token, user_data=user_data_to_update
            )

        with step("Checking the response code"):
            assert_status_code(updating_user_response, 400)

        with step("Checking the response type of the body"):
            assert_content_type(updating_user_response, "application/json")

        with step("Checking the response message"):
            assert_response_message(updating_user_response, expected_message)

    @pytest.mark.parametrize(
        "first_name_length, last_name_length, expected_message",
        [
            pytest.param(
                1,
                8,
                "First name must be at least 2 characters long",
                marks=pytest.mark.xfail(
                    reason="BUG: IL-232: User First Name Accepts Less Than Minimum Required Characters"
                ),
            ),
            pytest.param(
                129,
                8,
                "First name cannot be longer than 128 characters",
                marks=pytest.mark.xfail(
                    reason="BUG: IL-233: Server Error on Updating User with Long First Name"
                ),
            ),
            pytest.param(
                8,
                1,
                "Last name must be at least 2 characters long",
                marks=pytest.mark.xfail(
                    reason="BUG: IL-232: User First Name Accepts Less Than Minimum Required Characters"
                ),
            ),
            pytest.param(
                8,
                129,
                "Last name cannot be longer than 128 characters",
                marks=pytest.mark.xfail(
                    reason="BUG: IL-233: Server Error on Updating User with Long First Name"
                ),
            ),
        ],
    )
    def test_update_user_first_name_length(
            self,
            create_authorized_user,
            first_name_length,
            last_name_length,
            expected_message,
    ):
        token = create_authorized_user["token"]

        with step("Generating new user data"):
            user_data_to_update = generate_user(
                first_name_length=first_name_length, last_name_length=last_name_length
            )

        with step("Updating user info via API"):
            updating_user_response = UsersAPI().update_user(
                token=token, user_data=user_data_to_update
            )

        with step("Checking the response code"):
            assert_status_code(updating_user_response, 400)

        with step("Checking the response type of the body"):
            assert_content_type(updating_user_response, "application/json")

        with step("Checking the response message"):
            assert_response_message(updating_user_response, expected_message)

    @title("Updating User's Wrong Birth Date")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to update their own birth date in wrong format, "
        "THEN the response code is 400 and the response body contains the error message."
    )
    def test_update_user_with_wrong_birth_date(self, create_authorized_user):
        token = create_authorized_user["token"]

        with step("Generating new user data"):
            user_data_to_update = generate_user()
            user_data_to_update["birthDate"] = "02-02-2010"

        with step("Updating user info via API"):
            updating_user_response = UsersAPI().update_user(
                token=token, user_data=user_data_to_update
            )

        with step("Checking the response code"):
            assert_status_code(updating_user_response, 400)

        with step("Checking the response type of the body"):
            assert_content_type(updating_user_response, "application/json")

        with step("Checking the response message"):
            assert_that(updating_user_response.json()["error"], is_("Bad Request"))

    @pytest.mark.xfail(
        reason="BUG:https://trello.com/c/7cPxzfaQ/4-update-users-info-format-error-message "
    )
    @title("Updating User's Birth Date with Empty Body")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to update their info with empty body, "
        "THEN the response code is 400 and the response body contains the error message."
    )
    def test_update_user_with_empty_body(self, create_authorized_user):
        token = create_authorized_user["token"]

        with step("Updating user info via API"):
            updating_user_response = UsersAPI().update_user(token=token, user_data={})

        with step("Checking the response code"):
            assert_status_code(updating_user_response, 400)

        with step("Checking the response type of the body"):
            assert_content_type(updating_user_response, "application/json")

        with step("Checking the response message"):
            assert_response_message(updating_user_response, "Request body is empty")
            assert_message_in_response(updating_user_response, "ErrorMessage: must not be null")
