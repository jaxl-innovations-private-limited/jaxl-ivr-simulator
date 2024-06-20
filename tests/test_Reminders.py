"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.Reminders import (
JaxlIVRRemindersWebhook,        
MAIN_MENU_PROMPT,
get_service_prompt,
confirm_service        
)




from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase



class TestCalculator(BaseJaxlIVRWebhookTestCase):
    """Test cases for Calculator IVR."""

    webhook_klass = JaxlIVRRemindersWebhook

    def setUp(self) -> None:
        super().setUp()

        # Start the call to webhook during setup
        self.start_call()

    def test_main_menu(self) -> None:
        """Test main menu prompt is returned as expected after start of call."""
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "Reminders")
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)

    def test_options(self) -> None:
        """Test relevant operations get triggered when 1, 2, 3, 4 is chosen by the user."""
        for option in ("1", "2", "3", "4"):
            _request, response = self.choose_option(option)
            self.assertEqual(response["prompt"], get_service_prompt
            (option))
            self.assertEqual(response["num_characters"], "*")
            self.assertEqual(response["stream"], None)

    def test_operation_on_user_input(self) -> None:
        """Test we get expected reply for addition request sent by user."""
        numbers = [12, 232, 2431]
        for option in ("1", "2", "3", "4"):
            user_input = "#".join(str(num) for num in numbers) + "*"
            expected_answer = confirm_service
            (option, numbers)
            _request, response = self.choose_option_and_send(option, user_input)
            self.assertEqual(
                response["prompt"],
                [
                    "The answer is",
                    str(expected_answer),
                ],
            )
            self.assertEqual(response["num_characters"], "*")
            self.assertEqual(response["stream"], None)

    def test_user_input_with_hash_followed_by_star(self) -> None:
        """While in motion, user may end the input with # followed by * via keypad.
        Ideally this is incorrect format.  IVR calculator anticipates such human errors and
        delivers the expected response"""
        _request, response = self.choose_option_and_send("1", "#12#232#2431#*")
        self.assertEqual(response["prompt"], ["The answer is", "2675"])
        self.assertEqual(response["num_characters"], "*")
        self.assertEqual(response["stream"], None)

    def test_user_input_with_repeated_hash(self) -> None:
        """While in motion, user may enter multiple hashes via keypad.
        Ideally this is incorrect format.  IVR calculator anticipates such human errors and
        delivers the expected response"""
        _request, response = self.choose_option_and_send("1", "12###232##2431*")
        self.assertEqual(response["prompt"], ["The answer is", "2675"])
        self.assertEqual(response["num_characters"], "*")
        self.assertEqual(response["stream"], None)
    