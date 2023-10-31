from allure import description, feature, link, step, title
from hamcrest import assert_that, is_, has_key, equal_to
import requests
from framework.endpoints.registration_api import generate_user_data


@feature("Registration user")
@link(
    url="https://github.com/Sunagatov/Online-Store/wiki",
    name="Description of the tested functionality",
)
class TestRegistration:
    @title("Registration user with valid credential")
    @description(
        "WHEN user registration with valid credential"
        "THEN  the status HTTP CODE = 201"
    )
    def test_successful_registration(self):
        with step("Creating a random user for http request "):
            data = generate_user_data()

        with step("Creating POST method for new user"):
            response = requests.post('http://localhost:8083/api/v1/auth/register', json=data)

        with step("Checking response"):
            assert_that(response.status_code, is_(201))

    @title("Registration user with exist credential")
    @description(
        "WHEN user registration with exist credential"
        "THEN the status HTTP CODE = 400"
    )
    def test_registration_with_exist_user(self):
        with step("Creating a random user for http request "):
            data = generate_user_data()

        with step("Creating POST method for new user"):
            requests.post('http://localhost:8083/api/v1/auth/register', json=data)

        with step("Creating POST method with the same data"):
            # Try to registration again with the same data
            response = requests.post('http://localhost:8083/api/v1/auth/register', json=data)

            assert_that(response.status_code, is_(400))
