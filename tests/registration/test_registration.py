import pytest
from allure import description, feature, link, step, title, severity
from hamcrest import assert_that, is_, has_length, has_key, is_not, empty

from framework.asserts.registration_asserts import check_mapping_api_to_db
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.steps.registration_steps import RegistrationSteps
from framework.tools.generators import generate_string


@feature("Registration of user")
@link(
    url="https://github.com/Sunagatov/Online-Store/wiki/",
    name="(!) WAIT LINK. Description of the tested functionality",
)
class TestRegistration:
    email = None
    user_to_register = None

    def setup_method(self):
        """
        Generate data for registration and user registration
        """
        with step("Generation data for registration and user registration"):
            self.email = generate_string(length=10, additional_characters=["@te.st"])
            first_name = generate_string(length=2)
            last_name = generate_string(length=2)
            password = generate_string(
                length=8, additional_characters=["@1"]
            ).capitalize()

            self.user_to_register = RegistrationSteps().data_for_sent(
                email=self.email,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

    @severity(severity_level="CRITICAL")
    @title("User registration under minimum requirements")
    @description(
        "WHEN the user submits the minimum required data for registration, "
        "THEN the information about the user is stored in the database"
    )
    def test_of_registration(self, postgres):
        with step("Registration of user"):
            registration_response = AuthenticateAPI().registration(body=self.user_to_register)

        with step("Checking the response code"):
            assert_that(registration_response.status_code, is_(201))

        with step("Checking the response body"):
            response_json = registration_response.json()
            assert_that(response_json["token"], is_not(empty()))

        with step("Getting info about the user in DB"):
            user_data = postgres.get_data_by_filter(
                table="user_details", field="email", value=self.email
            )

        with step("Checking mapping data from the API request to the database"):
            check_mapping_api_to_db(api_request=self.user_to_register, database_data=user_data[0])

    @pytest.mark.skip(reason="Bug in the API => wrong error message for not unique email")
    @severity(severity_level="MAJOR")
    @title("User registration with not unique email")
    @description(
        "WHEN the user submits data with a non-unique email for registration, "
        "THEN the user receives an error message, and the user's information is not stored in the database"
    )
    def test_of_registration_email_uniqueness(self, postgres):
        with step("Registration of user"):
            registration_response = AuthenticateAPI().registration(body=self.user_to_register)
            assert_that(registration_response.status_code, is_(201))

        with step("Registration of user's duplicate"):
            duplicate_registration_response = AuthenticateAPI().registration(body=self.user_to_register)

        with step("Checking the response code"):
            assert_that(duplicate_registration_response.status_code, is_(400))

        with step("Checking the response body"):
            expected_message = 'Email must be unique'
            response_json = duplicate_registration_response.json()
            assert_that(response_json["message"][0], is_(expected_message))

        with step("Getting info about the user with not unique email in DB"):
            user_data = postgres.get_data_by_filter(
                table="user_details", field="email", value=self.email
            )

        with step("Checking that new user with duplicate email has not been registered "):
            assert_that(user_data, has_length(1))
            check_mapping_api_to_db(api_request=self.user_to_register, database_data=user_data[0])

    fields = [
        # ("email", "Email should have a length between 2 and 128 characters"),
        ("firstName", "First name is the mandatory attribute"),
        ("lastName", "Last name is the mandatory attribute"),
        ("password", "Password is the mandatory attribute")
    ]

    @pytest.mark.skip(reason="Bug in the API => wrong error message for missing required field")
    @pytest.mark.parametrize("data", fields)
    @severity(severity_level="MAJOR")
    @title("User registration with missing required field")
    @description(
        f"WHEN the user submits data with a missing required field for registration, "
        "THEN the user receives an error message, and the user's information is not stored in the database"
    )
    def test_of_registration_required_fields(self, postgres, data):
        with step("Preparing data for registration"):
            [field, expected_message] = data
            self.user_to_register.pop(field)

        with step("Registration of user"):
            registration_response = AuthenticateAPI().registration(body=self.user_to_register)

        with step("Checking the response code"):
            assert_that(registration_response.status_code, is_(400))

        with step("Checking the response body"):
            response_json = registration_response.json()
            assert_that(response_json["message"][0], is_(expected_message))

        with step(f"Checking that new user with missing field {field} has not been registered "):
            user_data = postgres.get_data_by_filter(
                table="user_details", field="email", value=self.email
            )
            assert_that(user_data, has_length(0))
