"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.
All rights reserved.
Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.welcome_greeting import JaxlIVRWelcomegreetingWebhook
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestJaxlIVRWelcomegreetingWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRWelcomegreetingWebhook IVR."""

    webhook_klass = JaxlIVRWelcomegreetingWebhook

    def setUp(self) -> None:
        super().setUp()

        # Start the call to webhook during setup
        self.start_call()

    def test_main_menu(self) -> None:
        """Tests main menu of your IVR i.e. response returned by start_call operation.

        Response of start_call is available as `self.start_call_response`.
        """
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "welcome_greeting")
        self.assertEqual(self.start_call_response["prompt"][0], "Welcome to Jaxl Innovations!")
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)
