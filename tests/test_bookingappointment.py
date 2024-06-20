"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.
All rights reserved.
Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from webhooks.bookingappointment import(
    JaxlIVRBookingappointmentWebhook,
    MAIN_MENU_PROMPT,
    get_operation_prompt,
)
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase

class TestJaxlIVRBookingappointmentWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRBookingappointmentWebhook IVR."""

    webhook_klass = JaxlIVRBookingappointmentWebhook

    def setUp(self) -> None:
        super().setUp()
        # Start the call to webhook during setup
        self.start_call()

    def test_main_menu(self) -> None:
        """Tests main menu of your IVR i.e. response returned by start_call operation.
        
        Response of start_call is available as `self.start_call_response`.
        """
        assert self.start_call_request and self.start_call_response
        self.assertEqual(self.start_call_request["name"], "bookingappointment")
        self.assertEqual(self.start_call_response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(self.start_call_response["num_characters"], 1)
        self.assertEqual(self.start_call_response["stream"], None)

    def test_choose_option_1(self) -> None:
        """Test selecting option 1 for new appointment."""
        _request, response = self.choose_option("1")
        self.assertEqual(response["prompt"], get_operation_prompt("1"))
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_choose_option_2(self) -> None:
        """Test selecting option 2 to cancel appointment."""
        _request, response = self.choose_option("2")
        self.assertEqual(response["prompt"], get_operation_prompt("2"))
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_choose_option_3(self) -> None:
        """Test selecting option 3 to reschedule appointment."""
        _request, response = self.choose_option("3")
        self.assertEqual(response["prompt"], get_operation_prompt("3"))
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_choose_option_4(self) -> None:
        """Test selecting option 4 to confirm existing appointment."""
        _request, response = self.choose_option("4")
        self.assertEqual(response["prompt"], get_operation_prompt("4"))
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_choose_option_0_star(self) -> None:
        """Test selecting option 0* to repeat the main menu."""
        _request, response = self.choose_option("0*")
        self.assertEqual(response["prompt"], MAIN_MENU_PROMPT)
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)

    def test_invalid_option(self) -> None:
        """Test selecting an invalid option."""
        _request, response = self.choose_option("9")
        self.assertEqual(response["prompt"], ["Invalid input! Invalid choice. Please try again.", "Press 1 for New appointment.", "Press 2 for Cancel appointment.", "Press 3 for Reschedule appointment.", "Press 4 for Confirm your existing appointment.", "Press 0 followed by a star sign to repeat this menu"])
        self.assertEqual(response["num_characters"], 1)
        self.assertEqual(response["stream"], None)
