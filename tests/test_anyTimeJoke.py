"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.
All rights reserved.
Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.anyTimeJoke import JaxlIVRAnytimejokeWebhook
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestJaxlIVRAnytimejokeWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRAnytimejokeWebhook IVR."""

    webhook_klass = JaxlIVRAnytimejokeWebhook

    def setUp(self) -> None:
        super().setUp()

        # Start the call to webhook during setup
        self.start_call()

    def test_main_menu(self) -> None:
        """Tests main menu of your IVR i.e. response returned by start_call operation.

        Response of start_call is available as `self.start_call_response`.
        """
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "anyTimeJoke")
        self.assertEqual(self.start_call_response["prompt"][0], "Welcome to the Joke of the Day IVR!")
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)

    def test_choose_option_1(self) -> None:
        """Test selecting option 1 to hear a joke."""
        _request, response = self.choose_option("1")
        self.assertIn("Here's your joke:", response["prompt"][0])
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_choose_option_0(self) -> None:
        """Test selecting option 0 to repeat the main menu."""
        _request, response = self.choose_option("0")
        self.assertEqual(response["prompt"][0], "Welcome to the Joke of the Day IVR!")
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_invalid_option(self) -> None:
        """Test selecting an invalid option."""
        _request, response = self.choose_option("5")
        self.assertEqual(response["prompt"][0], "Invalid choice. Please try again.")
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)
