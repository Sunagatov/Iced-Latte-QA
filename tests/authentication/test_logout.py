from allure import feature, description, link, step, title
from hamcrest import assert_that, is_

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.steps.registration_steps import RegistrationSteps
from framework.tools.generators import generate_string


@feature("Logout of a user")
@link(
    url="https://github.com/Sunagatov/Online-Store/wiki/",
    name="(!) WAIT LINK. Description of the tested functionality",
)
class TestLogout:
    @title("Checking log out")
    @description(
        "GIVEN the user is logged in, WHEN the user logout, THEN the JWT token is not valid"
    )
    def test_logout(self, postgres):
        with step("Generation data for registration"):
            email = generate_string(length=2, additional_characters=["@te.st"])
            first_name = generate_string(length=2)
            last_name = generate_string(length=2)
            password = generate_string(
                length=8, additional_characters=["@1"]
            ).capitalize()

            body = RegistrationSteps().data_for_sent(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

        with step("Registration of user"):
            response_registration = AuthenticateAPI().registration(body=body)
            assert_that(response_registration.status_code, is_(201))

        with step("Getting info about the random user in DB"):
            data_user = postgres.get_random_users()[0]

        with step("Authentication of user"):
            token = (
                AuthenticateAPI()
                .authentication(email=email, password=password)
                .json()["token"]
            )

        with step("Getting user info by ID via API"):
            user = UsersAPI().get_user_by_id(token=token, user_id=data_user["id"])
            assert_that(
                user.status_code, is_(200), reason='Failed request "get_user_by_id"'
            )

        with step("Log out of user"):
            log_out = AuthenticateAPI().logout(token=token)
            assert_that(log_out.status_code, is_(200), reason='Failed request "logout"')

        with step("Re-getting data user by ID via API"):
            user = UsersAPI().get_user_by_id(token=token, user_id=data_user["id"])

        with step("Checking the response from the API"):
            assert_that(user.status_code, is_(401), reason="Log out not executed")
            assert_that(
                user.json()["Description"],
                is_("Invalid token. Try authenticating again"),
                reason="Description does not match",
            )
