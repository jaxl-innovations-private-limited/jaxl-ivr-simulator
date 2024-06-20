"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.emergency_info import (
    EmergencyInfoIVRWebhook,
    MAIN_MENU_PROMPT,
)
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestEmergencyInfoIVR(BaseJaxlIVRWebhookTestCase):
    """Test cases for Emergency Information Hotline IVR."""

    webhook_klass = EmergencyInfoIVRWebhook

    def setUp(self) -> None:
        super().setUp()

        self.start_call()

    def test_main_menu(self) -> None:
        """Test main menu prompt is returned as expected after start of call."""
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "emergency_info")
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)

    def test_options(self) -> None:
        """Test relevant responses get triggered when 1, 2, 3, or 0 is chosen by the user."""
        options_responses = {
            "1": ["For medical emergencies, please stay calm and call 100."],
            "2": ["For fire emergencies, please evacuate the building immediately and call 100."],
            "3": ["For police emergencies, please call 100."],
            "0": ["Please wait while we connect you to an operator."]
        }
        
        for option, expected_prompt in options_responses.items():
            _request, response = self.choose_option(option)
            self.assertEqual(response["prompt"], expected_prompt)
            self.assertEqual(response["num_characters"], 1)
            self.assertEqual(response["stream"], None)

    def test_invalid_option(self) -> None:
        """Test response for invalid option chosen by the user."""
        _request, response = self.choose_option("9")
        self.assertEqual(response["prompt"], ["Invalid choice. Returning to the main menu."])
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)
