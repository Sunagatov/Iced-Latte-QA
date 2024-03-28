from assertpy import assert_that as assertpy_assert_that
from requests import Response


def assert_deleted_item_ids_in_response(
    response: Response, ids_to_check: list[dict]
) -> None:
    """Checking deleted items in the request API

    Args:
          response:  The API response object, expected to contain a JSON body with product information.
          ids_to_check: dictionary with list deleted product ids .
    """
    try:
        response_data = response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not in valid JSON format: {e}") from e

    item_ids = [item["id"] for item in response_data.get("items", [])]
    for id_to_check in ids_to_check:
        assertpy_assert_that(item_ids).does_not_contain(id_to_check)


def assert_added_product_not_in_api_response(
    response: Response, added_products: list[dict]
) -> None:
    """
    Asserts that none of the products specified in added_products are present in the API response.

    Args:
        added_products: A list of dictionaries, each containing 'productId' and 'productQuantity' keys
                        for products added to the user's shopping cart.
        response: The API response object, expected to contain a JSON body with product information.
    """

    try:
        response_data = response.json()
    except ValueError as e:
        raise AssertionError(f"Response is not in valid JSON format: {e}") from e

    response_product_ids = [
        item["productInfo"]["id"] for item in response_data["items"]
    ]

    added_product_ids = [product["productId"] for product in added_products]

    for added_product_id in added_product_ids:
        assertpy_assert_that(response_product_ids).does_not_contain(added_product_id)
