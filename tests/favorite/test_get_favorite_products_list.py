import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, none, empty, any_of, is_, is_not

from framework.asserts.assert_favorite import (
    assert_id_key_and_its_value_is_not_empty_in_response,
)
from framework.asserts.common import assert_content_type
from framework.endpoints.favorite_api import FavoriteAPI


@feature("Get info about favorite products ")
class TestFavorite:
    @pytest.mark.critical
    @title("Test get info about not created list of favorite products")
    @description(
        "GIVEN user is registered and does not have favorite products list"
        "WHEN user get info about favorite products list"
        "THEN status HTTP CODE = 200 and response body contains info about favorite 'products' list = null"
    )
    def test_getting_info_about_not_created_favorite_products_list(
        self, create_authorized_user
    ):
        with step("Registration of user"):
            user, token = (
                create_authorized_user["user"],
                create_authorized_user["token"],
            )

        with step("Get info about favorite products"):
            response_get_favorites = FavoriteAPI().get_favorites(token=token)

        with step("Verify that user's favorite 'products' list = null"):
            favorite_product_info = response_get_favorites.json().get("products")
            assert_that(favorite_product_info, any_of(is_(none()), empty()))

        with step("Verify content-type"):
            assert_content_type(response_get_favorites, "application/json")

    @pytest.mark.critical
    @pytest.mark.parametrize("product_quantity", [4], indirect=True)
    @title("Test get info about created list of favorite products")
    @description(
        "GIVEN user is registered and has favorite products list.len=2"
        "WHEN user get info about favorite products list"
        "THEN status HTTP CODE = 200 and response body contains info about favorite products list"
    )
    def test_getting_info_about_created_favorite_products_list(
        self, add_product_to_favorite_list
    ):
        with step("Add random product to the favorite list"):
            (
                token,
                _,
            ) = add_product_to_favorite_list

        with step("Get info about favorite products list"):
            response_get_favorites = FavoriteAPI().get_favorites(token=token)

        with step("Verify that user's  favorite products list not None"):
            favorite_product_list_info = response_get_favorites.json().get("products")
            assert_that(favorite_product_list_info, any_of(is_not(none()), empty()))
            assert_id_key_and_its_value_is_not_empty_in_response(response_get_favorites)

        with step("Verify content-type"):
            assert_content_type(response_get_favorites, "application/json")
