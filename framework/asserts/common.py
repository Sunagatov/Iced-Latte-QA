from hamcrest import assert_that, is_, contains_string


def assert_status_code(response, expected_status_code):
    """
    Asserts that the actual status code matches the expected status code.

    :param response: The response object from the API call.
    :param expected_status_code: The expected status code.
    """
    assert_that(response.status_code, is_(expected_status_code),
                reason=f"Expected status code {expected_status_code}, found: {response.status_code}")


def assert_content_type(response, expected_content_type):
    """
    Asserts that the Content-Type of the response matches the expected Content-Type.

    :param response: The response object from the API call.
    :param expected_content_type: The expected Content-Type string.
    """
    content_type = response.headers.get('Content-Type', '')
    assert_that(content_type, contains_string(expected_content_type),
                reason=f"Expected Content-Type '{expected_content_type}', found: '{content_type}'")


def assert_response_message(response, expected_message):
    """
    Asserts that the message in the response body matches the expected message.

    :param response: The response object from the API call.
    :param expected_message: The expected message string.
    """
    actual_message = response.json().get("message", "")
    assert_that(actual_message, is_(expected_message),
                reason=f"Expected message '{expected_message}', found: '{actual_message}'")


def assert_message_in_response(response, expected_message):
    """
    Asserts that the message in the response body matches the expected message.

    :param response: The response object from the API call.
    :param expected_message: The expected message string.
    """
    actual_message = response.json().get("message", "")
    assert_that(actual_message, contains_string(expected_message),
                reason=f"Expected response contains '{expected_message}', found: '{actual_message}'")
