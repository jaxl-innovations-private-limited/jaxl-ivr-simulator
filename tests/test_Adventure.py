"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.adventure import (
    JaxlIVRAdventureWebhook,
    MAIN_MENU_PROMPT,
    get_adventure_prompt,
)
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase

class TestAdventureGame(BaseJaxlIVRWebhookTestCase):
    """Test cases for Adventure Game IVR."""

    webhook_klass = JaxlIVRAdventureWebhook

    def setUp(self) -> None:
        super().setUp()
        self.start_call()

    def test_main_menu(self) -> None:
        """Test main menu prompt is returned as expected after start of call."""
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "adventure")  # Ensure the name is adventure
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)

    def test_options(self) -> None:
        """Test relevant paths get triggered when 1, 2, 3 are chosen by the user."""
        for option in ("1", "2", "3"):
            _request, response = self.choose_option(option)
            self.assertEqual(response["prompt"], get_adventure_prompt(option))
            self.assertEqual(response["num_characters"], 1)
            self.assertEqual(response["stream"], None)

    def test_choose_path(self) -> None:
        """Test user can choose paths and receive appropriate prompts."""
        paths_to_test = {
            "1": "1_1",  # Choosing path 1 leads to 1_1
            "2": "2_1",  # Choosing path 2 leads to 2_1
            "3": "3_1",  # Choosing path 3 leads to 3_1
        }

        for initial_path, chosen_path in paths_to_test.items():
            _request, response = self.choose_option_and_send(initial_path, "1*")
            self.assertEqual(response["prompt"], get_adventure_prompt(chosen_path))

    def test_invalid_choice(self) -> None:
        """Test invalid choice handling."""
        _request, response = self.choose_option_and_send("4", "1*")
        self.assertEqual(response["prompt"], ["Invalid choice. Please try again."])
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_invalid_data_format(self) -> None:
        """Test invalid data format handling."""
        _request, response = self.choose_option_and_send("2", "invalid*")
        self.assertEqual(response["prompt"], ["Invalid choice. Please try again."])
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_repeat_menu(self) -> None:
        """Test repeating the main menu."""
        _request, response = self.choose_option_and_send("0", "0*")
        self.assertEqual(response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)
