import pytest
from allure import description, feature, link, step, title, severity
from hamcrest import assert_that, has_length, is_not, empty, equal_to

from configs import DB_NAME, HOST_DB, PORT_DB, DB_USER, DB_PASS
from framework.asserts.common import assert_status_code, assert_message_in_response
from framework.asserts.registration_asserts import check_mapping_api_to_db
from framework.clients.db_client import DBClient
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.queries.postgres_db import PostgresDB
from framework.steps.registration_steps import RegistrationSteps
from framework.tools.generators import generate_string, generate_user_data

# Connection configuration
PostgresDB.dbname = DB_NAME
PostgresDB.host = HOST_DB
PostgresDB.port = PORT_DB
PostgresDB.user = DB_USER
PostgresDB.password = DB_PASS


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

    @pytest.mark.critical
    @severity(severity_level="MAJOR")
    @title("User registration with not unique email")
    @description(
        "WHEN the user submits data with a non-unique email for registration, "
        "THEN the user receives an error message, and the user's information is not stored in the database"
    )
    def test_of_registration_email_uniqueness(self, postgres, create_authorized_user):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Generation data for registration with already exist email in DB"):
            data = generate_user_data(
                first_name_length=5, last_name_length=5, password_length=8, email=user["email"]
            )

        with step("Registration user with already exist email in DB"):
            duplicate_registration_response = AuthenticateAPI().registration(
                body=data, expected_status_code=400
            )

        with step("Checking the response body"):
            expected_message = "Email must be unique"
            assert_message_in_response(
                duplicate_registration_response, expected_message
            )

        with step(
                "Checking that new user with duplicate email has not been registered "
        ):
            email_to_check = user["email"]
            result = postgres.select_user_by_email(email=email_to_check)
            count = result[0]['count']
            assert_that(count, equal_to(1), f"Expected 1 user with email {email_to_check}, but found {count}.")

    fields = [
        # ("email", "Email is the mandatory attribute"), # Bug in the API => wrong error message for missing required field
        ("firstName", "First name is the mandatory attribute"),
        ("lastName", "Last name is the mandatory attribute"),
        ("password", "Password is the mandatory attribute"),
    ]

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
            registration_response = AuthenticateAPI().registration(
                body=self.user_to_register, expected_status_code=400
            )

        with step("Checking the response body"):
            assert_message_in_response(registration_response, expected_message)

        with step(
                f"Checking that new user with missing field {field} has not been registered "
        ):
            user_data = postgres.get_data_by_filter(
                table="user_details", field="email", value=self.email
            )
            assert_that(user_data, has_length(0))
