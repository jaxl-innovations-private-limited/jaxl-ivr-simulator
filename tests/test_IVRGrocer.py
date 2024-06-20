"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.IVRGrocer import (
    JaxlIVRIvrgrocerWebhook,
    MAIN_MENU_PROMPT,
    CART,
    PRODUCTS_AVAILABLE,
)

from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestJaxlIVRIvrgrocerWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRIvrgrocerWebhook IVR."""

    webhook_klass = JaxlIVRIvrgrocerWebhook

    def setUp(self) -> None:
        super().setUp()

        # Start the call to webhook during setup
        self.start_call()

    def test_main_menu(self) -> None:
        """Test main menu prompt is returned as expected after start of call."""
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "IVRGrocer")
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], "*")
        self.assertEqual(self.start_call_response["stream"], None)

    def test_return_to_main_menu(self) -> None:
        """Test case when user wants to listen to main menu again"""
        _request, response = self.choose_option("#*")
        self.assertEqual(response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(response["num_characters"], "*")
        self.assertEqual(response["stream"], None)

    def test_list_cart_items(self) -> None:
        """Test Case when user wants to listen to elements in cart currently"""
        items_in_cart = ""
        for item in CART["items"]:
            items_in_cart = items_in_cart + " " + item
        _request, response = self.choose_option("0*")

        self.assertEqual(
            response["prompt"],
            [
                "You have opted to view the contents of your cart:",
                f"Products currently in your cart are {items_in_cart}",
                f"Total amount {CART['total_price']} rupees",
                "To return to the main menu, please enter #*",
            ],
        )
        self.assertEqual(response["num_characters"], "*")
        self.assertEqual(response["stream"], None)

    def test_addition_of_item(self) -> None:
        """Test case when user adds a valid product id and wants to add it to cart for first time"""
        for option in ("1*", "2*", "3*", "4*"):
            productId = option[0]
            choosenProduct = PRODUCTS_AVAILABLE[productId]
            _request, response = self.choose_option(option)
            self.assertEqual(
                response["prompt"],
                [
                    f"You have opted to add the product {choosenProduct['product_name']}.",
                    f"{choosenProduct['product_name']} is priced {choosenProduct['price']} rupees.",
                    f"Product {choosenProduct['product_name']} added successfully.",
                    "To return to the main menu, please enter #*",
                ],
            )
            self.assertEqual(response["num_characters"], "*")
            self.assertEqual(response["stream"], None)

    def test_addition_of_item_when_item_already_in_cart(self) -> None:
        """Test case when user adds a valid product id and wants to add it to cart
        after adding it already one time before"""
        for option in ("1*", "2*", "3*", "4*"):
            _request, response = self.choose_option(option)
            self.assertEqual(
                response["prompt"],
                ["Item Already in the Cart"],
            )
            self.assertEqual(response["num_characters"], "*")
            self.assertEqual(response["stream"], None)

    def test_other_input(self) -> None:
        """Test case when user enters any other option then listed ones"""
        for option in ("**", "00000*0*", "37*", "5*", "***", "##*"):
            _request, response = self.choose_option(option)
            self.assertEqual(response["prompt"], ["Please check your input again."])
            self.assertEqual(response["num_characters"], "*")
            self.assertEqual(response["stream"], None)
