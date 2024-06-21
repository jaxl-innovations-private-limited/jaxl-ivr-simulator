"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.lite_Banking import JaxlIVRLitebankingWebhook
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestJaxlIVRLitebankingWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRLitebankingWebhook IVR."""

    webhook_klass = JaxlIVRLitebankingWebhook

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
