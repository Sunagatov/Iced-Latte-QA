import pytest
from allure import description, step, title, feature, severity
from hamcrest import assert_that, not_, is_not, empty

from configs import (
    gmail_password,
    imap_server,
    email_address_to_connect,
    EMAIL_DOMAIN,
    EMAIL_LOCAL_PART,
)
from configs import password, firstName, lastName, email, email_iced_late
from framework.asserts.common import assert_content_type
from framework.asserts.registration_asserts import check_mapping_api_to_db
from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI

from framework.tools.class_email import Email
from framework.tools.generators import (
    generate_string,
    append_random_to_local_part_email,
)


#
# Connection configuration
# PostgresDB.dbname = DB_NAME
# PostgresDB.host = HOST_DB
# PostgresDB.port = PORT_DB
# PostgresDB.user = DB_USER
# PostgresDB.password = DB_PASS


@feature("Registration of user")
class TestAuthentication:
    @pytest.mark.critical
    @severity(severity_level="CRITICAL")
    @title("Test registration user with email confirmation")
    @description(
        "WHEN the user submits the minimum required data for registration,"
        "WHEN registration's confirmation code from email is provided"
        "THEN status HTTP CODE = 200 and get JWT token"
    )
    def test_registration(self, postgres):
        with step("Generation data for registration"):
            email_random = append_random_to_local_part_email(
                domain=EMAIL_DOMAIN,
                email_local_part=EMAIL_LOCAL_PART,
                length_random_part=5,
            )
            data_for_registration = {
                "firstName": firstName,
                "lastName": lastName,
                "password": password,
                "email": email_random,
            }

        with step("Registration new user"):
            response_registration = AuthenticateAPI().registration(
                body=data_for_registration
            )
            expected_content_type = "text/plain;charset=UTF-8"
            assert_content_type(
                response_registration, expected_content_type=expected_content_type
            )

        with step("Extract code from email for confirmation registration"):
            email_box = "Inbox"
            key = "from_"
            value = email_iced_late
            code_from_email = Email(
                imap_server=imap_server,
                email_address=email_address_to_connect,
                mail_password=gmail_password,
            ).extract_confirmation_code_from_email(
                email_box=email_box, key=key, value=value
            )
            assert_that(code_from_email, not_(None), "Token should not be empty")

        with step("Confirm registration using code from email"):
            response_after_confirmation = AuthenticateAPI().confirmation_email(
                code=code_from_email
            )

        with step("Verify JWT token is returned after confirmation and content type"):
            assert_that(response_after_confirmation.json()["token"], is_not(empty()))
            expected_content_type = "application/json"
            assert_content_type(
                response_after_confirmation, expected_content_type=expected_content_type
            )

        with step(
            "Verify that user is successfully registered by getting info about user"
        ):
            UsersAPI().get_user(token=response_after_confirmation.json()["token"])

        with step(
            "Verify that user is successfully registered by authentication through user's credentials"
        ):
            email_for_authentication = data_for_registration["email"]
            password_for_authentication = data_for_registration["password"]

            response_authentication = AuthenticateAPI().authentication(
                email=email_for_authentication, password=password_for_authentication
            )
            expected_content_type = "application/json"
            assert_content_type(
                response_authentication, expected_content_type=expected_content_type
            )
            token = response_authentication.json().get("token")

        with step("Getting info about the user in DB"):
            user_data = postgres.get_data_by_filter(
                table="user_details",
                field="email",
                value=data_for_registration["email"],
            )

        with step("Checking mapping data from the API request to the database"):
            check_mapping_api_to_db(
                api_request=data_for_registration, database_data=user_data[0]
            )

        with step("Deleting user"):
            UsersAPI().delete_user(token=token)
