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

    for key_api, key_db in fields_api_to_db.items():
        if key_api == "password":
            # Hash the password from the API request
            hashed_password = bcrypt.hashpw(api_request[key_api].encode('utf-8'), database_data[key_db].encode('utf-8'))
            assert_that(
                hashed_password.decode('utf-8'),
                is_(database_data[key_db]),
                reason=f'"{key_db}" not equal expected',
            )
        else:
            assert_that(
                api_request[key_api],
                is_(database_data[key_db]),
                reason=f'"{key_db}" not equal expected',
            )
