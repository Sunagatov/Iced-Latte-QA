from hamcrest import assert_that, is_
import bcrypt


def check_mapping_api_to_db(api_request: dict, database_data: dict) -> None:
    """Checking the mapping of data from the request API to the database

    Args:
        api_request:    reference data, data from an API request;
        database_data:  compared data, data from the database (a dictionary).
    """
    fields_api_to_db = {
        "email": "email",
        "firstName": "first_name",
        "lastName": "last_name",
        "password": "password",
    }
    # Hash the password
    api_request["password"] = bcrypt.hashpw(
        api_request["password"].encode("utf-8"),
        database_data["password"].encode("utf-8"),
    ).decode("utf-8")

    for key_api, key_db in fields_api_to_db.items():
        assert_that(
            api_request[key_api],
            is_(database_data[key_db]),
            reason=f'"{key_db}" not equal expected',
        )
