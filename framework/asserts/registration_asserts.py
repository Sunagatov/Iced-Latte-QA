from hamcrest import assert_that, is_


def check_mapping_api_to_db(api_request: dict, database_data: dict) -> None:
    """Checking the mapping of data from the request API to database

    Args:
        api_request:    reference data, data from an API-request;
        database_data:  compared data, data from database.
    """
    fields_api_to_db = {
        "email": "email",
        "firstName": "first_name",
        "lastName": "last_name",
        "password": "password",
    }
    for key_api, key_db in fields_api_to_db.items():
        assert_that(
            api_request[key_api],
            is_(database_data[key_db]),
            reason=f'"{key_db}" not equal expected',
        )
