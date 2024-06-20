"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.query_resolver import JaxlIVRQueryresolverWebhook
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestJaxlIVRQueryresolverWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRQueryresolverWebhook IVR."""

    webhook_klass = JaxlIVRQueryresolverWebhook

    def setUp(self) -> None:
        super().setUp()

        # Start the call to webhook during setup
        self.start_call()

    def test_main_menu(self) -> None:
        """Tests main menu of your IVR i.e. response returned by start_call operation.

        Response of start_call is available as `self.start_call_response`.
        """
        expected_prompt = (
            "Welcome to the smartphone troubleshooting system. "
            "Press 1 for network issues, 2 for speaker issues, "
            "3 for battery issues, 4 for app issues, "
            "5 for system settings."
        )
        self.assertEqual(self.start_call_response.prompt, expected_prompt)

    def test_handle_option_network(self) -> None:
        """Test handling of network issue selection."""
        self.send_dtmf('1')
        expected_prompt = "You selected network issues. Please describe your issue."
        response = self.get_next_response()
        self.assertEqual(response.prompt, expected_prompt)
        self.assertEqual(response.next_state, 'network_issue')

    def test_handle_option_speaker(self) -> None:
        """Test handling of speaker issue selection."""
        self.send_dtmf('2')
        expected_prompt = "You selected speaker issues. Please describe your issue."
        response = self.get_next_response()
        self.assertEqual(response.prompt, expected_prompt)
        self.assertEqual(response.next_state, 'speaker_issue')

    def test_handle_option_battery(self) -> None:
        """Test handling of battery issue selection."""
        self.send_dtmf('3')
        expected_prompt = "You selected battery issues. Please describe your issue."
        response = self.get_next_response()
        self.assertEqual(response.prompt, expected_prompt)
        self.assertEqual(response.next_state, 'battery_issue')

    def test_handle_option_app(self) -> None:
        """Test handling of app issue selection."""
        self.send_dtmf('4')
        expected_prompt = "You selected app issues. Please describe your issue."
        response = self.get_next_response()
        self.assertEqual(response.prompt, expected_prompt)
        self.assertEqual(response.next_state, 'app_issue')

    def test_handle_option_system(self) -> None:
        """Test handling of system setting issue selection."""
        self.send_dtmf('5')
        expected_prompt = "You selected system settings. Please describe your issue."
        response = self.get_next_response()
        self.assertEqual(response.prompt, expected_prompt)
        self.assertEqual(response.next_state, 'system_setting')

    def test_handle_option_invalid(self) -> None:
        """Test handling of invalid selection."""
        self.send_dtmf('9')
        expected_prompt = (
            "Invalid selection. Press 1 for network issues, "
            "2 for speaker issues, 3 for battery issues, "
            "4 for app issues, 5 for system settings."
        )
        response = self.get_next_response()
        self.assertEqual(response.prompt, expected_prompt)
        self.assertEqual(response.next_state, 'handle_option')
