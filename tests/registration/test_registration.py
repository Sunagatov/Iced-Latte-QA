from allure import description, feature, link, step, title
from hamcrest import assert_that, is_

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
    @title("User registration under minimum requirements")
    @description(
        "WHEN the user submits the minimum required data for registration, "
        "THEN the information about the user is stored in the database"
    )
    def test_of_registration(self, postgres):
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

        with step("Getting info about the user in DB"):
            user_data = postgres.get_data_by_filter(
                table="user_details", field="email", value=email
            )

        with step("Checking mapping data from the API request to the database"):
            check_mapping_api_to_db(api_request=body, database_data=user_data[0])
