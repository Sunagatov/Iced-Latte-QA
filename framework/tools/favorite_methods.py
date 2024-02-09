import random

from requests import Response


def extract_random_product_ids(response: Response, product_quantity: int) -> list:
    """ Extract random product IDs from the API response to add to favorites.

    Selects a random sample of products from the response based on the given quantity.
    Returns a list of the ID values for those randomly selected products.

    Args:
        response: Response data from API request containing products
        product_quantity: Number of random products to select

    Raises:
        ValueError: If requested quantity exceeds products available
    """
    products = response.json()["products"]
    if product_quantity > len(products):
        raise ValueError("Requested amount exceeds the number of available products")

    selected_products = random.sample(products, product_quantity)

    return [product['id'] for product in selected_products]
