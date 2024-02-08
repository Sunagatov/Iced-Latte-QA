import pytest
from allure import description, step, title, feature
from hamcrest import assert_that, empty, none, any_of, is_

from framework.asserts.assert_favorite import assert_added_product_in_favorites
from framework.asserts.common import assert_content_type
from framework.endpoints.favorite_api import FavoriteAPI
from framework.endpoints.product_api import ProductAPI
from framework.tools.favorite_methods import extract_random_product_ids


@feature("Adding product to favorite ")
class TestFavorite:

    @pytest.mark.critical
    @pytest.mark.skip(reason="BUG, user add product that not exist in BD or empty product's list [], status code should be = 400")
    @title("Test add products to favorite negative")
    @description(
        "GIVEN user is registered and does not have favorite list"
        "WHEN user add a products with incorrect/not exist id to favorite"
        "THEN status HTTP CODE = "
    )
    @pytest.mark.parametrize(
        "id_product_add_to_favorite, expected_status_code",
        [
            pytest.param(
                [],
                400
            ),
            pytest.param(
                ["12324456678888"],
                400
            ),
            pytest.param(
                ["ytyty8888GGG-jgjjggj6666-555GGGhhhjj"],
                400
            ),
            pytest.param(
                ["#$$%^&*@##$$%%^^&&&&&&*"],
                400
            ),
            pytest.param(
                ["fc88cd5d-5049-4b04-8d88-df1d974a3ce1"],
                400
            ),
        ],
    )
    def test_adding_product_with_incorrect_id_format_to_favorite(self, create_authorized_user,
                                                                 id_product_add_to_favorite, expected_status_code):
        with step("Registration of user"):
            user, token = create_authorized_user["user"], create_authorized_user["token"]

        with step("Verify that user does not have favorite list"):
            response_get_favorites = FavoriteAPI().get_favorites(token=token)
            favorite_product_info = response_get_favorites.json().get("products")
            assert_that(favorite_product_info, any_of(is_(none()), empty()))

        with step("Add product with incorrect id product to favorite"):
            product_list_add_to_favorite = id_product_add_to_favorite
            FavoriteAPI().add_favorites(token=token,
                                            favorite_product=product_list_add_to_favorite,
                                            expected_status_code=expected_status_code)

        with step("Verify that user's favorite 'products' list = null"):
            favorite_product_info = response_get_favorites.json().get("products")
            assert_that(favorite_product_info, any_of(is_(none()), empty()))
