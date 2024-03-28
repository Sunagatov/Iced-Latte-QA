import random
import pytest
from allure import description, step, title, feature

from framework.endpoints.favorite_api import FavoriteAPI


@feature("Delete product from favorite list ")
class TestFavorite:
    @pytest.mark.critical
    @pytest.mark.parametrize("product_quantity", [2], indirect=True)
    @title("Test delete product from favorite list")
    @description(
        "GIVEN user is registered has favorite products list"
        "WHEN user delete product from favorite list"
        "THEN status HTTP CODE = 200"
    )
    def test_deleting_product_from_favorite_list(self, add_product_to_favorite_list):
        with step("Registration of user"):
            token, product_list_added_to_favorite = add_product_to_favorite_list

        with step("Get info about user's favorite list"):
            response_get_favorites = FavoriteAPI().get_favorites(token=token)

        with step("Selecting random product from favorite list for deleting"):
            favorite_product_list_info_from_response = (
                response_get_favorites.json().get("products")
            )
            selected_product = random.choice(favorite_product_list_info_from_response)
            selected_id_product_to_delete = selected_product.get("id")

        with step("Deleting selected product from favorite list"):
            FavoriteAPI().delete_favorites(
                token=token, id_product=selected_id_product_to_delete
            )
