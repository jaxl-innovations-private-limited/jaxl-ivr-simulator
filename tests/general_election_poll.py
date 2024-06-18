"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

# from webhooks.calculator import JaxlIVRCalculatorWebhook
# from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase


# class TestJaxlIVRCalculatorWebhook(BaseJaxlIVRWebhookTestCase):
#     """Test cases for JaxlIVRCalculatorWebhook IVR."""

#     webhook_klass = JaxlIVRCalculatorWebhook

#     def setUp(self) -> None:
#         super().setUp()

#         # Start the call to webhook during setup
#         self.start_call()

#     def test_main_menu(self) -> None:
#         """Tests main menu of your IVR i.e. response returned by start_call operation.

#         Response of start_call is available as `self.start_call_response`.
#         """
#         # Complete me
#         self.assertEqual(1, 1)



from webhooks.general_election_poll import JaxlIVRGeneralElectionPollWebhook
from jaxl.ivr.frontend.base import BaseJaxlIVRWebhookTestCase

class TestJaxlIVRGeneralElectionPollWebhook(BaseJaxlIVRWebhookTestCase):
    """Test cases for JaxlIVRGeneralElectionPollWebhook IVR."""

    webhook_klass = JaxlIVRGeneralElectionPollWebhook

    def setUp(self) -> None:
        super().setUp()

        # Start the call to webhook during setup
        self.start_call()

    def test_main_menu(self) -> None:
        """Tests main menu of your IVR i.e. response returned by start_call operation.

        Response of start_call is available as `self.start_call_response`.
        """
        # Assert that the start call response is the main menu message
        self.assertEqual(
            self.start_call_response['message'],
            "Welcome to General Election of India 2024. Press 1 for Voting, Press 2 for Instructions, Press 3 for Exit."
        )

    def test_select_constituency(self) -> None:
        """Tests selection of constituency in the IVR."""
        # Simulate pressing 1 for Voting
        response = self.send_input("1")
        self.assertEqual(
            response['message'],
            "Please select your constituency. Press 1 for Constituency A, Press 2 for Constituency B, Press 3 for Constituency C."
        )

    def test_vote_constituency_a(self) -> None:
        """Tests voting in Constituency A."""
        # Simulate pressing 1 for Voting
        self.send_input("1")
        # Simulate pressing 1 for Constituency A
        response = self.send_input("1")
        self.assertEqual(
            response['message'],
            "You selected Constituency A. Press 1 to vote for Candidate X, Press 2 to vote for Candidate Y, Press 3 to vote for Candidate Z."
        )

    def test_vote_candidate_x(self) -> None:
        """Tests voting for Candidate X in Constituency A."""
        # Simulate pressing 1 for Voting
        self.send_input("1")
        # Simulate pressing 1 for Constituency A
        self.send_input("1")
        # Simulate pressing 1 to vote for Candidate X
        response = self.send_input("1")
        self.assertEqual(
            response['message'],
            "Thank you for your vote!"
        )

    def test_instructions(self) -> None:
        """Tests the instructions option in the IVR."""
        # Simulate pressing 2 for Instructions
        response = self.send_input("2")
        self.assertEqual(
            response['message'],
            "To participate in the General Election of India 2024, please press 1 for Voting, press 2 for Instructions, and press 3 for Exit."
        )

    def test_exit(self) -> None:
        """Tests the exit option in the IVR."""
        # Simulate pressing 3 for Exit
        response = self.send_input("3")
        self.assertEqual(
            response['message'],
            "Thank you for calling. Goodbye!"
        )
