import pytest
from allure import feature, description, link, step, title
from hamcrest import assert_that, is_, contains_string

from framework.asserts.user_asserts import assert_all_user_data_matches
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import generate_user


@feature("Getting user info by ID")
@link(
    url="https://github.com/Sunagatov/Online-Store/wiki/",
    name="(!) WAIT LINK. Description of the tested functionality",
)
class TestGetUserById:
    @title("Getting User's Own Information by ID")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to get their own information by ID, "
        "THEN the response code is 200 and the response body contains the current user's data."
    )
    def test_get_user_self_info_with_valid_id(self, create_authorized_user):
        user, token = [create_authorized_user["user"], create_authorized_user["token"]]

        with step("Getting user info by ID via API"):
            getting_user_response = UsersAPI().get_user_by_id(token=token, user_id=user["id"])

        with step("Checking the response code"):
            assert_that(
                getting_user_response.status_code, is_(200), reason='Status code should be 200'
            )

        with step("Checking the response body"):
            user_data = getting_user_response.json()
            assert_all_user_data_matches(user_data, user)

    @title("Getting Another User Info by ID")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to get information about another user by ID, "
        "THEN the response code is 200 and the response body contains the searched user's data"
    )
    def test_get_another_user_info_with_valid_id(self, postgres, create_authorized_user):
        token = create_authorized_user["token"]

        with step("Creating another user"):
            another_user = generate_user()
            postgres.create_user(another_user)

        with step("Getting another user info by ID via API"):
            getting_user_response = UsersAPI().get_user_by_id(token=token, user_id=another_user["id"])

        with step("Checking the response code"):
            assert_that(
                getting_user_response.status_code, is_(200), reason='Status code should be 200'
            )

        with step("Checking the response body"):
            user_data = getting_user_response.json()
            assert_all_user_data_matches(user_data, another_user)

    @pytest.mark.skip(reason="NEED TO CLARIFY: Bug in the API => wrong response type (text instead of JSON)")
    @title("Getting User Info by ID with Invalid Token")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to get user information by ID using an invalid token, "
        "THEN the response code is 401 and the response body contains an appropriate error message."
    )
    def test_get_user_info_with_invalid_token(self, create_user):
        user = create_user
        invalid_token = "invalid_token"

        with step("Getting user info by ID"):
            getting_user_response = UsersAPI().get_user_by_id(token=invalid_token, user_id=user["id"])
            print(getting_user_response.json())

        with step("Checking the response code"):
            assert_that(
                getting_user_response.status_code, is_(401), reason='Status code should be 401'
            )

        with step("Checking the Content-Type"):
            content_type = getting_user_response.headers.get('Content-Type', '')
            assert_that(
                content_type, contains_string('application/json'), reason='Content-Type should be JSON'
            )

        with step("Checking the response body"):
            expected_error_message = 'Internal server error'
            assert_that(
                getting_user_response.json()["message"], is_(expected_error_message),
                reason=f'Message should be "{expected_error_message}"'
            )


    # @title("Getting user info by ID with invalid ID")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about herself by invalid ID, "
    #     "THEN the response code is 404 and the response body contains the error message"
    # )
    # def test_getting_user_with_invalid_id(self, postgres):
    #     pass
    #
    # @title("Getting user info by ID with expired token")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about herself by ID with expired token, "
    #     "THEN the response code is 401 and the response body contains the error message"
    # )
    # def test_getting_user_with_expired_token(self, postgres):
    #     pass
    #
    # @title("Getting user info by ID with empty token")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about herself by ID with empty token, "
    #     "THEN the response code is 401 and the response body contains the error message"
    # )
    # def test_getting_user_with_empty_token(self, postgres):
    #     pass
    #
    # @title("Getting user info by ID with empty ID")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about herself by empty ID, "
    #     "THEN the response code is 404 and the response body contains the error message"
    # )
    # def test_getting_user_with_empty_id(self, postgres):
    #     pass
    #
    # @title("Getting user info by ID with invalid ID type")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about herself by invalid ID type, "
    #     "THEN the response code is 404 and the response body contains the error message"
    # )
    # def test_getting_user_with_invalid_id_type(self, postgres):
    #     pass
    #
    #
    # @title("Getting user info by ID with blacklisted token")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about herself by ID with blacklisted token, "
    #     "THEN the response code is 401 and the response body contains the error message"
    # )
    # def test_getting_user_with_blacklisted_token(self, postgres):
    #     pass
    #
    # @title("Getting user info by ID with token not containing email")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about herself by ID with token not containing email, "
    #     "THEN the response code is 401 and the response body contains the error message"
    # )
    # def test_getting_user_with_token_not_containing_email(self, postgres):
    #     pass
    #
    # @title("Getting user info by ID with token not containing user ID")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about herself by ID with token not containing user ID, "
    #     "THEN the response code is 401 and the response body contains the error message"
    # )
    # def test_getting_user_with_token_not_containing_user_id(self, postgres):
    #     pass
    #
    # @title("Getting user info by ID with token containing invalid email")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about herself by ID with token containing invalid email, "
    #     "THEN the response code is 401 and the response body contains the error message"
    # )
    # def test_getting_user_with_token_containing_invalid_email(self, postgres):
    #     pass
