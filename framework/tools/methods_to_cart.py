from hamcrest import assert_that, equal_to, has_key


def verify_products_in_response(response) -> list:
    """Extracts product info from a response.

    Iterates through the items in the response and extracts the product ID,
    quantity for each item into a list of dictionaries.

    Args:
       response: The response to extract products from

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


def assert_compare_product_to_add_with_response(add_product: list[dict], expected_product: list[dict]):
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


def extract_item_id(response):
    try:
        response_data = response.json()
    except ValueError:

        return {"error": "Invalid JSON response"}

    extracted_ids = []

    for item in response_data.get('items', []):
        item_id = item.get('id')
        if item_id:
            extracted_ids.append(item_id)

    return {"shoppingCartItemIds": extracted_ids}


def extract_define_quantity_items_id(response, num_items_to_delete=None):
    # Initialize an empty list to store the extracted information
    try:
        response_data = response.json()
    except ValueError:
        # Handle cases where JSON decoding fails
        return {"error": "Invalid JSON response"}

    extracted_ids = []

    # Iterate through each item in the 'items' list
    for item in response_data.get('items', []):
        # Extract item ID and add to the list
        item_id = item.get('id')
        if item_id:
            extracted_ids.append(item_id)

    if num_items_to_delete is not None:
        extracted_ids = extracted_ids[:num_items_to_delete]
    return {"shoppingCartItemIds": extracted_ids}



