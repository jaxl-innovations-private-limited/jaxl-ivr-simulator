"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.mobile_opd import (
    JaxlIVRMobileopdWebhook,
    MAIN_MENU_PROMPT,
    GENERAL_OPD_PROMPT,
    OPHTHALMOLOGY_OPD_PROMPT,
    SEVERITY_PROMPT,
    GENERAL_ADVICE
)
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


class TestMobileOPD(BaseJaxlIVRWebhookTestCase):
    """Test cases for Mobile OPD IVR."""

    webhook_klass = JaxlIVRMobileopdWebhook

    def setUp(self) -> None:
        super().setUp()

        # Start the call to webhook during setup
        self.start_call()

    def test_main_menu(self) -> None:
        """Test main menu prompt is returned as expected after start of call."""
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "mobile-opd")
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)

    def test_general_opd_menu(self) -> None:
        """Test general OPD menu is returned as expected after choosing option 1."""
        _request, response = self.choose_option("1")
        self.assertEqual(response["prompt"], GENERAL_OPD_PROMPT)
        self.assertEqual(response["num_characters"], "*")
        self.assertEqual(response["stream"], None)

    def test_ophthalmology_opd_menu(self) -> None:
        """Test ophthalmology OPD menu is returned as expected after choosing option 2."""
        _request, response = self.choose_option("2")
        self.assertEqual(response["prompt"], OPHTHALMOLOGY_OPD_PROMPT)
        self.assertEqual(response["num_characters"], "*")
        self.assertEqual(response["stream"], None)

    def test_severity_prompt(self) -> None:
        """Test severity prompt is returned after choosing illness."""
        _request, response = self.choose_option_and_send("1", "1*")
        self.assertEqual(response["prompt"], SEVERITY_PROMPT)
        self.assertEqual(response["num_characters"], "*")
        self.assertEqual(response["stream"], None)

    def test_mild_illness_advice(self) -> None:
        """Test advice is given for mild illness."""
        _request, response = self.choose_option_and_send("1", "1*")
        _request, response = self.choose_option_and_send("1", "1*")
        self.assertEqual(response["prompt"], [GENERAL_ADVICE["1"]])
        self.assertEqual(response["num_characters"], "*")
        self.assertEqual(response["stream"], None)

    def test_severe_illness_redirect(self) -> None:
        """Test redirection to doctor for severe illness."""
        _request, response = self.choose_option_and_send("1", "1*")
        _request, response = self.choose_option_and_send("1", "2*")
        self.assertEqual(response["prompt"], ["Your condition seems severe. Connecting you to a doctor."])
        self.assertEqual(response["num_characters"], "*")
        self.assertEqual(response["stream"], None)
