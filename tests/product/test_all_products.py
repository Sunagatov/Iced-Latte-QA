import pytest

from allure import description, feature, link, step, title
from hamcrest import assert_that, is_
from random import randint

from framework.asserts.product_asserts import check_mapping_db_to_api
from framework.endpoints.product_api import ProductAPI


@feature("Getting a list of all products")
@link(
    url="https://github.com/Sunagatov/Online-Store/wiki/API-Specification-for-Product",
    name="Description of the tested functionality",
)
class TestAllProducts:
    @title("Getting all products not authorized")
    @description(
        "WHEN not authorized requesting to get all products without parameters, "
        "THEN all products from the list are returned"
    )
    def test_get_all_products_not_auth(self, postgres):
        with step("Getting info about the random product in DB"):
            db_data = postgres.get_random_products()[0]

        with step("Getting all products via API"):
            api_data = ProductAPI().get_all()
            products = api_data.json()["products"]

        with step("Selecting an item from a list received via API by id"):
            assert_data = [el for el in products if el["id"] == db_data["id"]][0]

        with step("Checking mapping data DB <> API"):
            check_mapping_db_to_api(reference=db_data, compared=assert_data)

        with step("Checking count items DB <> API"):
            assert_that(len(db_data), is_(len(products)))

    @title("Getting all products with query parameters")
    @description(
        "WHEN not authorized requesting to get all products with query parameters, "
        "THEN the products sorted by attributes are returned"
    )
    @pytest.mark.parametrize(
        "params",
        [
            pytest.param({}, id="Default parameters"),
            pytest.param(
                {
                    "page": 0,
                    "size": 1,
                    "sort_attribute": "price",
                    "sort_direction": "desc",
                },
                id="?page=0&size=1&sort_attribute=price&sort_direction=desc",
            ),
            pytest.param(
                {
                    "page": 0,
                    "size": 1,
                    "sort_attribute": "name",
                    "sort_direction": "asc",
                },
                id="?page=0&size=1&sort_attribute=name&sort_direction=asc",
            ),
            pytest.param(
                {
                    "page": 1,
                    "size": 1,
                    "sort_attribute": "quantity",
                    "sort_direction": "desc",
                },
                id="?page=1&size=1&sort_attribute=quantity&sort_direction=desc",
            ),
            pytest.param(
                {
                    "page": 1,
                    "size": 1,
                    "sort_attribute": "price",
                    "sort_direction": "asc",
                },
                id="?page=1&size=1&sort_attribute=price&sort_direction=asc",
            ),
            pytest.param(
                {
                    "page": 1,
                    "size": 1,
                    "sort_attribute": "name",
                    "sort_direction": "desc",
                },
                id="?page=1&size=1&sort_attribute=name&sort_direction=desc",
            ),
            pytest.param(
                {
                    "page": 0,
                    "size": 1,
                    "sort_attribute": "quantity",
                    "sort_direction": "asc",
                },
                id="?page=0&size=1&sort_attribute=quantity&sort_direction=asc",
            ),
        ],
    )
    def test_get_all_products_with_params(self, params: dict, postgres):
        with step("Setting the parameters by default"):
            # These are the values required to query the database
            field = params["sort_attribute"] if params.get("sort_attribute") else "name"
            ascend = True if params.get("sort_direction") == "asc" else False
            size = params.get("size", 50)
            page = params.get("page", 0)

        with step("Getting products by query parameters via API"):
            api_data = ProductAPI().get_all(params=params).json()["products"]

        with step("Getting products by filters from DB"):
            db_data = postgres.get_product_by_filter(
                field=field, ascend=ascend, size=size, page=page
            )

        with step("Checking count items DB <> API"):
            assert_that(len(db_data), is_(len(api_data)))

        with step("Checking mapping data DB <> API"):
            index = randint(0, len(db_data) - 1)
            check_mapping_db_to_api(reference=db_data[index], compared=api_data[index])
