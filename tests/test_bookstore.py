"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.bookstore import (
   JaxlIVRBookstoreWebhook,
    MAIN_MENU_PROMPT,
    get_service_prompt,
    confirm_service,
)

from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase

class TestJaxlIVRBookstoreWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRBookstoreWebhook IVR."""

    webhook_klass = JaxlIVRBookstoreWebhook

    def setUp(self) -> None:
        super().setUp()
        self.start_call()

    def test_main_menu(self) -> None:
        """Test main menu prompt is returned as expected after start of call."""
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "bookstore")
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)

    def test_question_prompt(self) -> None:
        """Test relevant question is asked when option is chosen by the user."""
        for service_id in range(1, 3):
            _request, response = self.choose_option(str(service_id))
            self.assertEqual(response["prompt"], get_service_prompt(service_id))
            self.assertEqual(response["num_characters"], 1)
            self.assertEqual(response["stream"], None)

    def test_confirm_service(self) -> None:
        """Test checking the user's answer."""
        for service_id, correct_option in [(1, "1"), (2, "1"), (3, "2")]:
            _request, response = self.choose_option_and_send(str(service_id), correct_option)
            self.assertEqual(response["prompt"], ["Confirmed service!"])
            self.assertEqual(response["num_characters"], 1)
            self.assertEqual(response["stream"], None)

            _request, response = self.choose_option_and_send(str(service_id), "2")
            self.assertEqual(response["prompt"], ["Some error occurred"])
            self.assertEqual(response["num_characters"], 1)
            self.assertEqual(response["stream"], None)
