import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, empty, none, any_of, is_

from framework.asserts.assert_favorite import assert_added_product_in_favorites
from framework.asserts.common import assert_content_type
from framework.endpoints.favorite_api import FavoriteAPI
from framework.endpoints.product_api import ProductAPI
from framework.tools.favorite_methods import extract_random_product_ids


@pytest.mark.critical
@feature("Adding product to favorite ")
class TestFavorite:
    @title("Test add products to favorite")
    @description(
        "GIVEN user is registered and does not have favorite list"
        "WHEN user add a products to favorite"
        "THEN status HTTP CODE = 200 and response body  contains added product to favorite"
    )
    def test_adding_products_to_favorite(self, create_authorized_user):
        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )

        with step("Verify that user does not have favorite list"):
            response_get_favorites = FavoriteAPI().get_favorites(token=token)
            favorite_product_info = response_get_favorites.json().get("products")
            assert_that(favorite_product_info, any_of(is_(none()), empty()))

        with step("Getting all products via API"):
            response_get_product = ProductAPI().get_all()

        with step("Select and add random products to favorite"):
            product_list_add_to_favorite = extract_random_product_ids(
                response_get_product, product_quantity=4
            )
            response_add_to_favorite = FavoriteAPI().add_favorites(
                token=token, favorite_product=product_list_add_to_favorite
            )

        with step("Verify that response contain info about added products to favorite"):
            assert_added_product_in_favorites(
                response_add_to_favorite, product_list_add_to_favorite
            )

        with step("Verify content-type"):
            assert_content_type(response_add_to_favorite, "application/json")

        with step(
            "Get info about favorite products after add products to favorite list "
        ):
            response_get_favorites = FavoriteAPI().get_favorites(token=token)

        with step("Verify that response contain info about added products to favorite"):
            assert_added_product_in_favorites(
                response_get_favorites, product_list_add_to_favorite
            )
