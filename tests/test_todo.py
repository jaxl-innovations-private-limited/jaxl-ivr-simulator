"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""


from webhooks.todo import (
    JaxlIVRTodoWebhook,
    MAIN_MENU_PROMPT,
    get_operation_prompt 
)
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestJaxlIVRTodoWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRTodoWebhook IVR."""

    webhook_klass = JaxlIVRTodoWebhook

    def setUp(self) -> None:
        super().setUp()

        # Start the call to webhook during setup
        self.start_call()

    def test_main_menu(self) -> None:
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)
    
    def test_options(self) -> None:
        for option in ("1", "2", "3"):
            _request, response = self.choose_option(option)
            self.assertEqual(response["prompt"], get_operation_prompt(option))
            self.assertEqual(response["num_characters"], "*")
            self.assertEqual(response["stream"], None)