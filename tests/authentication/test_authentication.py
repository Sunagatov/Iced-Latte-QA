from allure import description, step, title, feature
from hamcrest import assert_that, is_, is_not, empty

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.generator_random_data import generate_user_data


@feature("Authentication of user")
class TestAuthentication:
    @title("Test authentication")
    @description(
        "WHEN user submit valid credential "
        "THEN status HTTP CODE = 200 and get JWT token"
    )
    def test_authentication(self, postgres):
        with step("Generation data for registration"):
            data = generate_user_data(length_first_name=8, length_last_name=8, password_len=8)

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)
            assert_that(response.status_code, is_(201))

        with step("Authentication  user"):
            data_post = {
                "email": data["email"],
                "password": data["password"],
            }
            response = AuthenticateAPI().authentication(email=data_post["email"], password=data_post["password"])
            assert_that(response.status_code, is_(200))

        with step("Assert Response JSON  have a 'token' key"):
            token = response.json().get("token")
            assert_that(response.json()['token'], is_not(empty()))

        with step("Get id user from DB "):
            email = data['email']
            user_data = postgres.get_data_by_filter(
                table="user_details", field="email", value=email
            )
            id_user = user_data[0]["id"]

        with step("Validation token by retrieving user information via API request by user's ID "):
            response_get = UsersAPI().get_user_by_id(user_id=id_user, token=token)
            assert_that(response_get.status_code, is_(200))
