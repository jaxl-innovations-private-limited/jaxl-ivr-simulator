"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""
import random
from pathlib import Path
from typing import Any, Optional, Tuple

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)


MAIN_MENU_PROMPT = [
    "Welcome! Please choose an option:",
    "Press 1 for New appointment.",
    "Press 2 for Cancel appointment.",
    "Press 3 for Reschedule appointment.",
    "Press 4 for Confirm your existing appointment.",
    "Press 0 followed by a star sign to repeat this menu.",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

OPERATION_PROMPTS = {
    "1": ["You have chosen to book a new appointment. Please provide the details."],
    "2": ["You have chosen to cancel an appointment. Please provide the appointment ID."],
    "3": ["You have chosen to reschedule an appointment. Please provide the new details."],
    "4": ["You have chosen to confirm an existing appointment. Please provide the appointment ID."],
}

INVALID_OPTION_PROMPT = [
    "Invalid input! Invalid choice. Please try again.",
    "Press 1 for New appointment.",
    "Press 2 for Cancel appointment.",
    "Press 3 for Reschedule appointment.",
    "Press 4 for Confirm your existing appointment.",
    "Press 0 followed by a star sign to repeat this menu.",
]

def get_operation_prompt(option: str) -> list[str]:
    return OPERATION_PROMPTS.get(option, INVALID_OPTION_PROMPT)

class JaxlIVRBookingappointmentWebhook(BaseJaxlIVRWebhook):
    """bookingAppointment.json webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "bookingAppointment.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of Call")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        option = request["option"]
        
        if option == "0*":
            return MAIN_MENU
        
        if option in ("1", "2", "3", "4"):
            return JaxlIVRResponse(
                prompt=get_operation_prompt(option),
                num_characters=1,
                stream=None
            )
        
        return JaxlIVRResponse(
            prompt=INVALID_OPTION_PROMPT,
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
