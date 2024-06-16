"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.kbc_quiz import (
    JaxlIVRKbcquizWebhook,
    MAIN_MENU_PROMPT,
    get_question_prompt,
    check_answer,
)

from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestJaxlIVRKbcquizWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRKbcquizWebhook IVR."""

    webhook_klass = JaxlIVRKbcquizWebhook

    def setUp(self) -> None:
        super().setUp()
        self.start_call()

    def test_main_menu(self) -> None:
        """Test main menu prompt is returned as expected after start of call."""
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "kbc_quiz")
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)

    def test_question_prompt(self) -> None:
        """Test relevant question is asked when option is chosen by the user."""
        for question_id in range(1, 5):
            _request, response = self.choose_option(str(question_id))
            self.assertEqual(response["prompt"], get_question_prompt(question_id))
            self.assertEqual(response["num_characters"], 1)
            self.assertEqual(response["stream"], None)

    def test_check_answer(self) -> None:
        """Test checking the user's answer."""
        for question_id, correct_option in [(1, "2"), (2, "3"), (3, "1"), (4, "3")]:
            _request, response = self.choose_option_and_send(str(question_id), correct_option)
            self.assertEqual(response["prompt"], ["Correct!"])
            self.assertEqual(response["num_characters"], 1)
            self.assertEqual(response["stream"], None)

            _request, response = self.choose_option_and_send(str(question_id), "4")
            self.assertEqual(response["prompt"], ["Incorrect. The correct answer was " + correct_option])
            self.assertEqual(response["num_characters"], 1)
            self.assertEqual(response["stream"], None)
