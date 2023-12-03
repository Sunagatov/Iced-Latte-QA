from hamcrest import assert_that, is_


def assert_user_data_matches(response_data: dict, expected_user: dict) -> None:
    """Asserts that all relevant user data in the response matches the expected user data.

    Args:
        response_data: The user data from the API response.
        expected_user: The expected user data.

    Raises:
        AssertionError: If any of the assertions fail.
    """

    fields = [key for key in response_data if key != "address"]

    assert_partial_match(expected_user, response_data, fields)


def assert_update_user_data_matches(response_data: dict, expected_user: dict) -> None:
    """Asserts that all relevant user data in the response matches the expected user data.

    Args:
        response_data: The user data from the API response.
        expected_user: The expected user data.

    Raises:
        AssertionError: If any of the assertions fail.
    """

    fields = ["firstName", "lastName", "birthDate", "phoneNumber"]

    assert_partial_match(expected_user, response_data, fields)


def assert_partial_match(expected: dict, actual: dict, fields_to_compare: list) -> None:
    """
    Asserts that the specified fields in the actual object match those in the expected object.

    Args:
        expected: The object with expected values.
        actual: The object to compare against the expected values.
        fields_to_compare: List of field names (str) to compare.
    """
    for field in fields_to_compare:
        assert_that(
            actual.get(field),
            is_(expected.get(field)),
            reason=f"Field {field} does not match. Expected: {expected.get(field)}, "
            f"Actual: {actual.get(field)}",
        )
