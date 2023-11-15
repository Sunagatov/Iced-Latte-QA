from allure import feature, description, link, step, title
from hamcrest import assert_that, is_

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI


@feature("Getting user info by ID")
@link(
    url="https://github.com/Sunagatov/Online-Store/wiki/",
    name="(!) WAIT LINK. Description of the tested functionality",
)
class TestGetUserById:
    @title("Getting user's herself info by ID")
    @description(
        "GIVEN the user is logged in, "
        "WHEN the user sends a request to get information about herself by ID, "
        "THEN the response code is 200 and the response body contains the current user's data"
    )
    def test_getting_current_user_with_valid_id(self, create_authorized_user):
        [user, token] = [create_authorized_user["user"], create_authorized_user["token"]]

        with step("Getting user info by ID via API"):
            getting_user_response = UsersAPI().get_user_by_id(token=token, user_id=user["id"])

        with step("Checking the response code"):
            assert_that(
                getting_user_response.status_code, is_(200), reason='Response code does not equal 200'
            )

        with step("Checking the response body"):
            response_json = getting_user_response.json()
            assert_that(response_json["id"], is_(user["id"]), reason='User ID does not match')
            assert_that(response_json["firstName"], is_(user["first_name"]), reason='User first name does not match')
            assert_that(response_json["lastName"], is_(user["last_name"]), reason='User last name does not match')
            assert_that(response_json["stripeCustomerToken"], is_(None), reason='User stripe customer token does not '
                                                                                'match')
            assert_that(response_json["email"], is_(user["email"]), reason='User email does not match')
            assert_that(response_json["password"], is_(user["hashed_password"]), reason='User password does not match')
            assert_that(response_json["address"], is_(None), reason='User address does not match')

    # @title("Getting another user info by ID")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about another user by ID, "
    #     "THEN the response code is 200 and the response body contains the searched user's data"
    # )
    # def test_getting_user_with_valid_id(self, postgres):
    #     with step("Generation data 2 for registration"):
    #         email = generate_string(length=2, additional_characters=["@te.st"])
    #         first_name = generate_string(length=2)
    #         last_name = generate_string(length=2)
    #         password = generate_string(
    #             length=8, additional_characters=["@1"]
    #         ).capitalize()
    #
    #         body2 = RegistrationSteps().data_for_sent(
    #             email=email,
    #             first_name=first_name,
    #             last_name=last_name,
    #             password=password,
    #         )
    #
    #     with step("Registration of user 2"):
    #         response_registration2 = AuthenticateAPI().registration(body=body2)
    #         assert_that(response_registration2.status_code, is_(201))
    #
    #     with step("Getting user ID"):
    #         user_id = postgres.get_data_by_filter(
    #             table="user_details", field="email", value=email
    #         )[0]["id"]
    #
    #     with step("Generation data for registration"):
    #         email = generate_string(length=2, additional_characters=["@te.st"])
    #         first_name = generate_string(length=2)
    #         last_name = generate_string(length=2)
    #         password = generate_string(
    #             length=8, additional_characters=["@1"]
    #         ).capitalize()
    #
    #         body = RegistrationSteps().data_for_sent(
    #             email=email,
    #             first_name=first_name,
    #             last_name=last_name,
    #             password=password,
    #         )
    #
    #     with step("Registration of user"):
    #         response_registration = AuthenticateAPI().registration(body=body)
    #         assert_that(response_registration.status_code, is_(201))
    #
    #     with step("Getting token"):
    #         token = response_registration.json()["token"]
    #
    #     with step("Getting user info by ID via API"):
    #         user = UsersAPI().get_user_by_id(token=token, user_id=user_id)
    #         assert_that(
    #             user.status_code, is_(200), reason='Failed request "get_user_by_id"'
    #         )
    #
    #
    # @title("Getting user info by ID with invalid token")
    # @description(
    #     "GIVEN the user is logged in, "
    #     "WHEN the user sends a request to get information about herself by ID with invalid token, "
    #     "THEN the response code is 401 and the response body contains the error message"
    # )
    # def test_getting_user_with_invalid_token(self, postgres):
    #     pass
    #
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
