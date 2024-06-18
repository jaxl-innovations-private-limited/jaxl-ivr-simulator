"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.
All rights reserved.
Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.Adventure import (
    JaxlIVRAdventureWebhook,
    MAIN_MENU_PROMPT,
    get_option_prompt,
    confirm_option,
)
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestJaxlIVRAdventureWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRAdventureWebhook IVR."""

    webhook_klass = JaxlIVRAdventureWebhook

    def setUp(self) -> None:
        super().setUp()
        self.start_call()

    def test_main_menu(self) -> None:
        """Test main menu prompt is returned as expected after start of call."""
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "Adventure")
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)

    def test_option_prompt(self) -> None:
        """Test relevant option is asked when option is chosen by the user."""
        for option_id in range(1, 5):  # Adjust range based on number of options
            _request, response = self.choose_option(str(option_id))
            self.assertEqual(response["prompt"], get_option_prompt(option_id))
            self.assertEqual(response["num_characters"], 1)
            self.assertEqual(response["stream"], None)

    def test_confirm_option(self) -> None:
        """Test confirming the user's choice."""
        for option_id, correct_choice in [(1, "1"), (2, "1"), (3, "2"), (4, "2")]:
            _request, response = self.choose_option_and_send(str(option_id), correct_choice)
            self.assertEqual(response["prompt"], [f"You have chosen to {correct_choice}. Enjoy your adventure!"])
            self.assertEqual(response["num_characters"], 1)
            self.assertEqual(response["stream"], None)

            # Test incorrect choice
            _request, response = self.choose_option_and_send(str(option_id), "invalid")
            self.assertEqual(response["prompt"], ["Some error occurred"])  # Adjust as per error handling

