import pytest
from allure import description, step, title, feature
from allure import severity
from hamcrest import assert_that, equal_to

from framework.asserts.common import assert_response_message
from framework.endpoints.users_api import UsersAPI
from framework.queries.postgres_db import PostgresDB


@feature("Delete user")
class TestDeleteUser:
    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("Test delete user")
    @description(
        "GIVEN user is registered"
        "WHEN user sends a request to delete user"
        "THEN status HTTP CODE = 200"
    )
    def test_delete_user(self, create_authorized_user):
        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )

        with step("Delete user"):
            UsersAPI().delete_user(token=token, expected_status_code=200)

        with step("Verify that user is deleted through API."):
            response = UsersAPI().get_user(token=token, expected_status_code=404)
            assert_message = "User with the provided email does not exist"
            assert_response_message(response, assert_message)

        with step("Verify that user is not in BD"):
            result = PostgresDB().select_user_by_email(email=user["email"])
            count = result[0]["count"]
            assert_that(count, equal_to(0))
