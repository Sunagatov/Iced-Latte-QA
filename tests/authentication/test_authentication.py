import json
from framework.endpoints.users_api import UsersAPI
import postgres
import requests
from allure_commons._allure import description, link, step, title, feature
from hamcrest import assert_that, is_, has_key, is_not, empty

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.queries.postgres_db import PostgresDB
from framework.tools.generator_random_data import generate_user_data
from framework.endpoints.authenticate_api import AuthenticateAPI

postgresBD = PostgresDB()


@feature("Authentication of user")
@link(
    url="https://github.com/Sunagatov/Online-Store/wiki/API-Specification-for-Product",
    name="Description of the tested functionality",
)
class TestAuthentication:
    @title("Test authentication")
    @description(
        "WHEN user submit valid credential "
        "THEN  status HTTP CODE = 200 and get JWT token"
    )
    def test_authentication(self):
        with step("Generation data for registration"):
            data: dict = generate_user_data()

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

            "Assert Response JSON  have a 'token' key"
            assert_that(response.json(), has_key('token'))
            assert_that(response.json()['token'], is_not(empty()))
            token = response.json()["token"]

        with step("Get id user from DB "):
            email = data['email']
            user_data = postgresBD.get_data_by_filter(
                table="user_details", field="email", value=email
            )
            id_user = user_data[0]["id"]

        with step("Validation token by retrieving user information via API request by user's ID "):
            response_get = UsersAPI().get_user_by_id(user_id=id_user, token=token)
            print(response_get.json())
            assert_that(response_get.status_code, is_(200))

