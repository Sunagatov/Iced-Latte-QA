from allure import description, step, title, feature
from hamcrest import assert_that, is_, is_not, empty, has_key, has_length

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import generate_user_data


@feature("Authentication of user")
class TestAuthentication:
    @title("Test authentication")
    @description(
        "GIVEN user is registered"
        "WHEN user submit valid credential for authentication"
        "THEN status HTTP CODE = 200 and get JWT token"
    )
    def test_authentication(self, postgres):
        with step("Generation data for registration"):
            data = generate_user_data(
                first_name_length=8, last_name_length=8, password_length=8
            )
            email = data["email"]

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            user_data = postgres.get_data_by_filter(
                table="user_details", field="email", value=email
            )
            print(user_data)
            assert_that(user_data, has_length(1))
            assert_that(
                response.status_code, is_(201), reason="Expected status code 201"
            )

        with step("Authentication  user"):
            data_post = {
                "email": data["email"],
                "password": data["password"],
            }
            response = AuthenticateAPI().authentication(
                email=data_post["email"], password=data_post["password"]
            )
            assert_that(
                response.status_code, is_(200), reason="Expected status code 200"
            )

        with step("Assert Response JSON  have a 'token' key"):
            token = response.json().get("token")
            assert_that(token, is_not(empty()))

        with step("Get id user from DB "):
            email = data["email"]
            user_data = postgres.get_data_by_filter(
                table="user_details", field="email", value=email
            )

        with step("Validation token by retrieving user information via API request "):
            response = UsersAPI().get_user(token=token)
            assert_that(
                response.status_code, is_(200), reason="Expected status code 200"
            )
