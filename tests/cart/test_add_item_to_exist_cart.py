from allure import description, step, title, feature
from hamcrest import assert_that, is_, is_not, empty, has_key, has_length

from framework.endpoints.authenticate_api import AuthenticateAPI
from framework.endpoints.users_api import UsersAPI
from framework.tools.generators import generate_user_data
from framework.endpoints.cart_api import CartAPI


@feature("Adding item to cart ")
class TestCart:
    @title("Test add product/products to cart for already exist user")
    @description(
        "GIVEN user is registered and cart is created"
        "WHEN user add item/items to cart"
        "THEN status HTTP CODE = 201"
    )
    def test_adding_item_to_cart(self):
        with step("Authentication existing user "):
            data = {
                "email": "jane@example.com",
                "password": "pass54321"
            }

            response = AuthenticateAPI().authentication(email=data["email"], password=data["password"])

            assert_that(
                response.status_code, is_(200), reason="Expected status code 200"
            )
            token = response.json()["token"]
            print(token)

        with step("Get cart of user"):
            response_get_cart = CartAPI().get_user_cart(token=token)
            print(response_get_cart.json())
            item_quantity = response_get_cart.json()["itemsQuantity"]
            product_quantity = response_get_cart.json()["productsQuantity"]
            print(item_quantity)
            print(product_quantity)

        with step("Adding new product to cart "):
            add_product_quantity = 1
            response = CartAPI().add_new_item_to_cart(token=token, id_product='ad0ef2b7-816b-4a11-b361-dfcbe705fc96',
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
        with step("Update quantity of product"):
            response_update_quantity = CartAPI().update_quantity_product(token=token, quantity=2, item_id='ad0ef2b7-816b-4a11-b361-dfcbe705fc96')
            print(response_update_quantity.json())
        with step("Delete item from cart"):
            response_delete_item = CartAPI().delete_item_from_cart(token=token,
                                                                   item_id='5b9928f7-17cd-452d-b2f8-58ca63ca5671')
            print(response_delete_item.json())
