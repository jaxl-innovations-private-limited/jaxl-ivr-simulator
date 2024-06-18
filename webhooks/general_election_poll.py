"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from pathlib import Path
from typing import Any, Optional, Tuple

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)


# class JaxlIVRCalculatorWebhook(BaseJaxlIVRWebhook):
#     """calculator.json webhook implementation."""

#     @staticmethod
#     def config() -> ConfigPathOrDict:
#         return Path(__file__).parent.parent / "schemas" / "calculator.json"

#     def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
#         raise NotImplementedError()

#     def teardown(self, request: JaxlIVRRequest) -> None:
#         raise NotImplementedError()

#     def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
#         raise NotImplementedError()

#     def stream(
#         self,
#         request: JaxlIVRRequest,
#         chunk_id: int,
#         sstate: Any,
#     ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
#         raise NotImplementedError()

from pathlib import Path
from typing import Any, Optional, Tuple

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)

class JaxlIVRGeneralElectionPollWebhook(BaseJaxlIVRWebhook):
    """general_election_poll.json webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "general_election_poll.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        """Handle the initial setup of the IVR session."""
        message = "Welcome to General Election of India 2024. Press 1 for Voting, Press 2 for Instructions, Press 3 for Exit."
        return JaxlIVRResponse(message=message)

    def teardown(self, request: JaxlIVRRequest) -> None:
        """Handle the teardown of the IVR session."""
        # Any cleanup logic goes here
        pass

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        """Handle the different options selected by the user."""
        option = request.input
        if option == "1":
            message = "Please select your constituency. Press 1 for Constituency A, Press 2 for Constituency B, Press 3 for Constituency C."
        elif option == "2":
            message = "To participate in the General Election of India 2024, please press 1 for Voting, press 2 for Instructions, and press 3 for Exit."
        elif option == "3":
            message = "Thank you for calling. Goodbye!"
        else:
            message = "Invalid input. Please press 1 for Voting, Press 2 for Instructions, Press 3 for Exit."
        
        return JaxlIVRResponse(message=message)

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        """Handle the streaming of IVR steps based on user input."""
        sstate = sstate or {}
        stage = sstate.get('stage', 'main_menu')

        if stage == 'main_menu':
            option = request.input
            if option == "1":
                message = "Please select your constituency. Press 1 for Constituency A, Press 2 for Constituency B, Press 3 for Constituency C."
                sstate['stage'] = 'select_constituency'
            elif option == "2":
                message = "To participate in the General Election of India 2024, please press 1 for Voting, press 2 for Instructions, and press 3 for Exit."
                sstate['stage'] = 'main_menu'
            elif option == "3":
                message = "Thank you for calling. Goodbye!"
                sstate['stage'] = 'end'
            else:
                message = "Invalid input. Please press 1 for Voting, Press 2 for Instructions, Press 3 for Exit."
                sstate['stage'] = 'main_menu'
        
        elif stage == 'select_constituency':
            option = request.input
            if option == "1":
                message = "You selected Constituency A. Press 1 to vote for Candidate X, Press 2 to vote for Candidate Y, Press 3 to vote for Candidate Z."
                sstate['stage'] = 'vote_constituency_a'
            elif option == "2":
                message = "You selected Constituency B. Press 1 to vote for Candidate A, Press 2 to vote for Candidate B, Press 3 to vote for Candidate C."
                sstate['stage'] = 'vote_constituency_b'
            elif option == "3":
                message = "You selected Constituency C. Press 1 to vote for Candidate P, Press 2 to vote for Candidate Q, Press 3 to vote for Candidate R."
                sstate['stage'] = 'vote_constituency_c'
            else:
                message = "Invalid input. Please select your constituency. Press 1 for Constituency A, Press 2 for Constituency B, Press 3 for Constituency C."
                sstate['stage'] = 'select_constituency'
        
        elif stage.startswith('vote_constituency'):
            message = "Thank you for your vote!"
            sstate['stage'] = 'end'
            # Here you would typically handle the vote and make a webhook call to record it
        
        if sstate['stage'] == 'end':
            return None
        
        return sstate, JaxlIVRResponse(message=message)

