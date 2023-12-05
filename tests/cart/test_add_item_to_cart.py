from allure import description, step, title, feature
from hamcrest import assert_that, is_, is_not, empty, has_key, has_length

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import generate_user_data
from framework.endpoints.cart_api import CartAPI
from framework.asserts.common import assert_response_message


@feature("Adding item to cart ")
class TestCart:
    @title("Test add item/items to cart")
    @description(
        "GIVEN user is registered"
        "WHEN "
        "THEN status HTTP CODE = "
    )
    def test_adding_item_to_cart(self):
        with step("Generation data for registration"):
            data = generate_user_data(
                first_name_length=8, last_name_length=8, password_length=8
            )

        with step("Registration new user"):
            response = AuthenticateAPI().registration(body=data)

            assert_that(
                response.status_code, is_(201), reason="Expected status code 201"
            )
            token = response.json()["token"]
            user_id = response.json().get("id")
            print(token)

            with step("Get cart of user"):
                response_get_cart = CartAPI().get_user_cart(token=token, expected_status_code=404)
                print(response_get_cart.json())
                expected_message = f'The shopping cart for the user with id = {user_id} is not found.'
                assert_response_message(response_get_cart, expected_message)

            with step("Adding new product to cart "):
                add_product_quantity = 1
                response = CartAPI().add_new_item_to_cart(token=token,
                                                          id_product='ad0ef2b7-816b-4a11-b361-dfcbe705fc96',
                                                          quantity=add_product_quantity)
                print(response.json())
                assert_that(
                    response.status_code, is_(200), reason="Expected status code 200"
                )
            with step("Verify cart after adding product to cart"):
                response_get_cart = CartAPI().get_user_cart(token=token)
                # print(response_get_cart.json())
                new_item_quantity = response_get_cart.json()["itemsQuantity"]
                new_product_quantity = response_get_cart.json()["productsQuantity"]
                print(new_item_quantity)
                print(new_product_quantity)

                # assert_that(new_product_quantity, is_(product_quantity + add_product_quantity),
                #             reason="Product quantity did not increase as expected")
                # assert_that(new_item_quantity, is_(product_quantity + add_product_quantity),
                #             reason="Product quantity did not increase as expected")
            # with step("Update quantity of product"):
            #     response_update_quantity = CartAPI().update_quantity_product(token=token, quantity=2,
            #                                                                  item_id='ad0ef2b7-816b-4a11-b361-dfcbe705fc96')
            #     print(response_update_quantity.json())
            # with step("Delete item from cart"):
            #     response_delete_item = CartAPI().delete_item_from_cart(token=token,
            #                                                            item_id='5b9928f7-17cd-452d-b2f8-58ca63ca5671')
            #     print(response_delete_item.json())
