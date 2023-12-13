from typing import List, Dict

from hamcrest import assert_that, equal_to, has_key


def get_product_info(response) -> List[Dict]:
    """Extracts product info (ID and quantity) from a response.

    Args:
       response: The JSON response.
    """
    response_data = response.json()
    extracted_products = []

    for item in response_data["items"]:
        product = item["productInfo"]
        product_info = {
            "id": product["id"],
            "productQuantity": item["productQuantity"]
        }

        extracted_products.append(product_info)
    return extracted_products


def assert_compare_product_to_add_with_response(add_product: List[Dict], expected_product: List[Dict]):
    """ Assertion that product were added to the shopping cart

    Args:
        add_product: list of products to add to the user's shopping cart
        expected_product: expected products from response
    """
    add_product_dict = {product['productId']: product for product in add_product}

    for expected in expected_product:
        expected_id = expected['id']
        expected_quantity = expected['productQuantity']

        assert_that(add_product_dict, has_key(expected_id),
                    f"Expected product with ID {expected_id} not found in add_product")

        matching_product = add_product_dict[expected_id]
        assert_that(matching_product['productQuantity'], equal_to(expected_quantity),
                    f"Quantity mismatch for product {expected_id}: Expected {expected_quantity}, found {matching_product['productQuantity']} in add_product")


def get_item_id(response) -> Dict:
    """ Gets item id from a JSON response.

    Args:
        response: The JSON response to extract ids from.
    Raises:
        ValueError: If JSON decoding of response fails.
    """
    try:
        response_data = response.json()
    except ValueError:

        return {"error": "Invalid JSON response"}

    extracted_ids = []

    for item in response_data.get('items', []):
        if item_id := item.get('id'):
            extracted_ids.append(item_id)

    return {"shoppingCartItemIds": extracted_ids}


def get_define_quantity_items_id(response, num_items_to_delete: int) -> Dict:
    """ Gets item ids from a JSON response.
    Args:
       num_items_to_delete: the quantity of items for delete
       response: The JSON response to extract ids from.
    Raises:
       ValueError: If JSON decoding of response fails.
    """

    try:
        response_data = response.json()
    except ValueError:
        return {"error": "Invalid JSON response"}

    extracted_ids = []

    for item in response_data.get('items', []):
        if item_id := item.get('id'):
            extracted_ids.append(item_id)

    if num_items_to_delete > 0:
        extracted_ids = extracted_ids[:num_items_to_delete]
    return {"shoppingCartItemIds": extracted_ids}
