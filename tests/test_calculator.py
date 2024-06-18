"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.calculator import JaxlIVRCalculatorWebhook
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestJaxlIVRCalculatorWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRCalculatorWebhook IVR."""

    webhook_klass = JaxlIVRCalculatorWebhook

    def setUp(self) -> None:
        super().setUp()

        # Start the call to webhook during setup
        self.start_call()

    def test_main_menu(self) -> None:
        """Tests main menu of your IVR i.e. response returned by start_call operation.

        Response of start_call is available as `self.start_call_response`.
        """
        # Complete me
        self.assertEqual(1, 1)
