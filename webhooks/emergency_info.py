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
    "Press 1 for Addition. ",
    "Press 2 for Subtraction. ",
    "Press 3 for Multiplication. ",
    "Press 4 for Division. ",
    "Press 0 followed by a star sign to repeat this menu",
]

from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)

MAIN_MENU_PROMPT = [
    "For medical emergencies, press 1. ",
    "For fire emergencies, press 2. ",
    "For police emergencies, press 3. ",
    "To speak to an operator, press 0.",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

class EmergencyInfoIVRWebhook(BaseJaxlIVRWebhook):
    """Emergency Information Hotline IVR webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "calculator.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of call")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        option = request["option"]

        if option == "1":
            return JaxlIVRResponse(
                prompt=[
                    "For medical emergencies, please stay calm and call 100. "
                ],
                num_characters=1,
                stream=None,
            )
        elif option == "2":
            return JaxlIVRResponse(
                prompt=[
                    "For fire emergencies, please evacuate the building immediately and call 100. "
                ],
                num_characters=1,
                stream=None,
            )
        elif option == "3":
            return JaxlIVRResponse(
                prompt=[
                    "For police emergencies, please call 112. "
                ],
                num_characters=1,
                stream=None,
            )
        elif option == "0":
            return JaxlIVRResponse(
                prompt=[
                    "Please wait while we connect you to an operator."
                ],
                num_characters=1,
                stream=None,
                dial="+1234567890"
            )
        else:
            return JaxlIVRResponse(
                prompt=["Invalid choice. Returning to the main menu."],
                num_characters=1,
                stream=None,
            )

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()
