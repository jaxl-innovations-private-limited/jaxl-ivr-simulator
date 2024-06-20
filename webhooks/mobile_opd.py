"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)

MAIN_MENU_PROMPT = [
    "Press 1 for General OPD. ",
    "Press 2 for Ophthalmology OPD. ",
    "Press 3 to check your medicine use case. ",
    "Press 4 to check appointment availability. ",
    "Press 5 to connect to a doctor. ",
    "Press 0 followed by a star sign to repeat this menu",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

GENERAL_OPD_PROMPT = [
    "Press 1 for Fever. ",
    "Press 2 for Other illness. ",
    "Press 0 followed by a star sign to repeat this menu",
]

OPHTHALMOLOGY_OPD_PROMPT = [
    "Press 1 for Eye Redness. ",
    "Press 2 for Other eye problems. ",
    "Press 0 followed by a star sign to repeat this menu",
]

SEVERITY_PROMPT = [
    "Press 1 if the illness is mild. ",
    "Press 2 if the illness is severe. ",
    "Press 0 followed by a star sign to repeat this menu",
]

OPTIONS_RESPONSES = {
    "1": GENERAL_OPD_PROMPT,
    "2": OPHTHALMOLOGY_OPD_PROMPT,
    "3": ["Please describe your medicine use case."],
    "4": ["Checking appointment availability. Please wait."],
    "5": ["Connecting you to a doctor. Please hold."]
}

GENERAL_ADVICE = {
    "1": "For mild fever, take rest and stay hydrated.",
    "2": "For mild symptoms, take over-the-counter medication and monitor your condition."
}

class JaxlIVRMobileopdWebhook(BaseJaxlIVRWebhook):
    """mobile-opd.json webhook implementation."""

    def __init__(self) -> None:
        super().__init__()
        self._current_operation: Optional[str] = None
        self._current_sub_operation: Optional[str] = None
        self._end_char = "*"
        self._separator = "#"

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "mobile-opd.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of call")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        if request.get("data", None) is not None:
            data = request["data"]
            assert data is not None
            assert data[-1] == self._end_char and self._current_operation
            # Repeat menu scenario
            if len(data) == 2 and data[0] == "0":
                self._current_operation = None
                self._current_sub_operation = None
                return MAIN_MENU
            if self._current_sub_operation:
                # Handle severity input
                if data.strip() == "1*":
                    return JaxlIVRResponse(
                        prompt=[GENERAL_ADVICE[self._current_sub_operation]],
                        num_characters=self._end_char,
                        stream=None,
                    )
                elif data.strip() == "2*":
                    return JaxlIVRResponse(
                        prompt=["Your condition seems severe. Connecting you to a doctor."],
                        num_characters=self._end_char,
                        stream=None,
                    )
                else:
                    return JaxlIVRResponse(
                        prompt=["Invalid input. Please try again."] + SEVERITY_PROMPT,
                        num_characters=self._end_char,
                        stream=None,
                    )
            else:
                # Handle illness type input
                self._current_sub_operation = data.strip()
                return JaxlIVRResponse(
                    prompt=SEVERITY_PROMPT,
                    num_characters=self._end_char,
                    stream=None,
                )

        self._current_operation = request["option"]
        if request["option"] in OPTIONS_RESPONSES:
            response_prompt = OPTIONS_RESPONSES[request["option"]]
            if isinstance(response_prompt, list):
                return JaxlIVRResponse(
                    prompt=response_prompt,
                    num_characters=self._end_char,
                    stream=None,
                )
            else:
                return JaxlIVRResponse(
                    prompt=[response_prompt],
                    num_characters=self._end_char,
                    stream=None,
                )
        return MAIN_MENU

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()
