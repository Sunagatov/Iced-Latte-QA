from allure import feature, description, link, step, title
from hamcrest import assert_that, is_

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI


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
    def test_logout(self, create_authorized_user):
        user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Log out of user"):
            logging_out_response = AuthenticateAPI().logout(token=token)
            assert_that(logging_out_response.status_code, is_(200), reason='Failed request "logout"')

        with step("Re-getting data user by ID via API"):
            getting_user_response = UsersAPI().get_user_by_id(token=token, user_id=user["id"])

        with step("Checking the response from the API"):
            assert_that(getting_user_response.status_code, is_(401), reason="Log out not executed")
            assert_that(
                getting_user_response.json()["message"],
                is_("JWT Token is blacklisted"),
                reason="Description does not match",
            )
