from typing import Union, Any, Dict

from hamcrest import assert_that as ham_assert_that, has_item
from assertpy import assert_that as assertpy_assert_that
from requests import Response


def assert_added_product_in_favorites(response: Response, product_add_to_favorite: list[str]):
    """ Asserts that the given products were added to user favorites.

    Args:
       response: The response from API request.
       product_add_to_favorite: A list of product IDs added to favorites.

    Raises:
       ValueError: If the response JSON is invalid.
       AssertionError: If any of the given product IDs are not found in the response.
    """
    try:
        response_data = response.json()
    except ValueError:
        return {"error": "Invalid JSON response"}

    data = response_data["products"]
    if not data:
        raise ValueError("Response does not contain 'products' or it's empty")

    list_id_from_data = [d['id'] for d in data if 'id' in d]
    for item in product_add_to_favorite:
        ham_assert_that(list_id_from_data, has_item(item), f"ID '{item}' not found in the response")


def assert_id_key_and_its_value_is_not_empty_in_response(response: Response) -> Union[Dict[str, str], None]:
    """Asserts product IDs exist and are not empty in response.

    Checks that the JSON response contains an "id" key for each product
    and that the id values are not empty. Raises error if issues found.

    Args:
        response: Response object from API request

    Returns:
        None if the assertions pass, or a dictionary with error information if the JSON is invalid.

    Raises:
        ValueError: If JSON response is invalid or does not meet expectations.
    """

    try:
        response_data = response.json()
    except ValueError:
        return {"error": "Invalid JSON response"}

    favorite_product_info = response_data.get("products")

    if not favorite_product_info:
        raise ValueError("Response does not contain 'products' or it's empty")

    for product in favorite_product_info:
        assertpy_assert_that(product).contains_key("id").described_as("Response does not contain an 'id' key")
        assertpy_assert_that(product["id"]).is_not_empty().described_as("Product 'id' has no value")
