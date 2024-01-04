import random
from typing import List, Dict, Any, Union
from hamcrest import assert_that, equal_to, has_key, not_, has_items, is_not, has_item, is_in
from requests import Response


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


def get_item_id(response) -> Union[dict, list]:
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

    return extracted_ids


def get_define_quantity_items_id(response: Response, num_items_to_delete: int) -> Dict:
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


def extract_items_details(response: Response) -> Union[dict, list]:
    """ Extracts item ID and product quantity from each item in the given JSON response.

    Args:
        response: The JSON response containing item details.
    """
    try:
        json_response = response.json()
    except ValueError:
        return {"error": "Invalid JSON response"}

    extracted_details = []

    for item in json_response.get('items', []):
        item_id = item.get('id', '')
        product_quantity = item.get('productQuantity', 0)
        extracted_details.append((item_id, product_quantity))

    return extracted_details


def extract_random_item_detail(response: Response) -> Dict:
    """ Extracts item ID and product quantity of a randomly selected item from the JSON response.

    Args:
        response: The JSON response containing item details.

   """
    try:
        json_response = response.json()
    except ValueError:
        return {"error": "Invalid JSON response"}

    items = json_response.get('items', [])

    if not items:
        raise ValueError("No items found in the JSON response.")

    random_item = random.choice(items)
    item_id = random_item.get('id', '')
    product_quantity = random_item.get('productQuantity', 0)
    return {
        "id": item_id,
        "productQuantity": product_quantity
    }


def get_quantity_specific_cart_item(response: Response, specific_item_id: str) -> Any:
    """ Extracts the quantity of a specific item from json response based on the provided specific ID.
    Args:
        response: The JSON response from request.
        specific_item_id: The specific ID of the item to find.

    Return: The quantity of the item with the specific ID, or a message if not found.
    """
    try:
        json_response = response.json()
    except ValueError:
        return {"error": "Invalid JSON response"}
    data = json_response.get("items", [])
    for item in data:
        if item.get('id') == specific_item_id:
            return item.get('productQuantity')
    return f"Item with ID {specific_item_id} not found."


