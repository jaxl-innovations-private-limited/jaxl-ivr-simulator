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

WELCOME_PROMPT = [
    "Welcome to Jaxl Innovations!",
    "Press 1 for customer service.",
    "Press 2 for technical support.",
    "Press 3 for sales inquiries.",
    "Press 0 followed by a star sign to repeat this menu.",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=WELCOME_PROMPT,
    num_characters=1,
    stream=None,
)

class JaxlIVRWelcomegreetingWebhook(BaseJaxlIVRWebhook):
    """welcome_greeting.json webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "welcome_greeting.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of Welcome Greeting")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        option = request["option"]
        
        if option == "0*":
            return MAIN_MENU
        
        elif option == "1":
            return JaxlIVRResponse(
                prompt=["You have selected customer service. Please hold on while we connect you."],
                num_characters=1,
                stream=None
            )
        
        elif option == "2":
            return JaxlIVRResponse(
                prompt=["You have selected technical support. Please hold on while we connect you."],
                num_characters=1,
                stream=None
            )
        
        elif option == "3":
            return JaxlIVRResponse(
                prompt=["You have selected sales inquiries. Please hold on while we connect you."],
                num_characters=1,
                stream=None
            )
        
        else:
            return JaxlIVRResponse(
                prompt=["Invalid input! Please try again."],
                num_characters=1,
                stream=None
            )

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()
