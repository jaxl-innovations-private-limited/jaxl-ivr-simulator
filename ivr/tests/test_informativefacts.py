"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.informativefacts import(JaxlIVRInformativefactsWebhook,MAIN_MENU_PROMPT,get_operation_prompt,) 
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestJaxlIVRInformativefactsWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRInformativefactsWebhook IVR."""

    webhook_klass = JaxlIVRInformativefactsWebhook

    def setUp(self) -> None:
        super().setUp()
        self.start_call()

    def test_main_menu(self) -> None:
        """Tests main menu of your IVR i.e. response returned by start_call operation.

        Response of start_call is available as `self.start_call_response`.
        """
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "informativefacts")
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)

    def test_choose_option_1(self) -> None:
        """Test selecting option 1 for fact about humans."""
        _request, response = self.choose_option("1")
        self.assertEqual(response["prompt"], get_operation_prompt("1"))
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_choose_option_2(self) -> None:
        """Test selecting option 2 for fact about animals."""
        _request, response = self.choose_option("2")
        self.assertEqual(response["prompt"], get_operation_prompt("2"))
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_choose_option_3(self) -> None:
        """Test selecting option 3 for facts about insects."""
        _request, response = self.choose_option("3")
        self.assertEqual(response["prompt"], get_operation_prompt("3"))
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_choose_option_4(self) -> None:
        """Test selecting option 4 for facts about plants."""
        _request, response = self.choose_option("4")
        self.assertEqual(response["prompt"], get_operation_prompt("4"))
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_choose_option_0_star(self) -> None:
        """Test selecting option 0 to repeat the main menu."""
        _request, response = self.choose_option("0")
        self.assertEqual(response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_invalid_option(self) -> None:
        """Test selecting an invalid option."""
        _request, response = self.choose_option("9")
        self.assertEqual(response["prompt"], ["Invalid input choice. Please try again.", "Press 1 for facts about humans.", "Press 2 for facts about animals.", "Press 3 for facts about insects.", "Press 4 for facts about plants", "Press 0 to repeat this menu"])
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)
