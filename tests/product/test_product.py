import uuid

from allure import description, feature, link, step, title
from hamcrest import assert_that, is_

from framework.asserts.common import assert_status_code, assert_response_message
from framework.asserts.product_asserts import check_mapping_db_to_api
from framework.endpoints.product_api import ProductAPI


@feature("Getting product info by ID")
class TestProduct:
    @title("Getting product info by ID not authorized")
    @description(
        "WHEN not authorized requesting to get product info by ID, THEN product info is returned"
    )
    def test_get_all_products(self, postgres):
        with step("Getting info about the random product in DB"):
            db_data = postgres.get_random_products()[0]

        with step("Getting product info by ID via API"):
            data = ProductAPI().get_by_id(_id=db_data["id"])
            assert_data = data.json()

        with step("Checking mapping data DB <> API"):
            check_mapping_db_to_api(reference=assert_data, compared=db_data)

    @title("Getting a non-existent product")
    @description(
        "WHEN requesting to get by a non-existent product ID, THEN the user receives a 404 status code"
    )
    def test_get_product(self):
        with step("Generating a non-existent ID"):
            non_exist_id = str(uuid.uuid4())

        with step(
            f'Getting product info by non-existent product ID via API "{non_exist_id}"'
        ):
            data = ProductAPI().get_by_id(_id=non_exist_id)

        with step("Checking response API"):
            assert_status_code(data, 404)
            expected_message = (
                f"The product with productId = {non_exist_id} is not found."
            )
            assert_response_message(data, expected_message)
