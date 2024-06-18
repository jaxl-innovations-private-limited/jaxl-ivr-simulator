"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.
All rights reserved.
Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from pathlib import Path
from typing import Any, List, Optional, Tuple

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)


MAIN_MENU_PROMPT = [
    "Press 1 to start your adventure. ",
    "Press 2 for more options. ",
    "Press 0 followed by a star sign to repeat this menu.",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

OPTIONS = {
    1: {
        "option": "Start your adventure",
        "choices": ["1. Explore the forest", "2. Enter the cave", "3. Climb the mountain"],
    },
    2: {
        "option": "More options",
        "choices": ["1. Visit the village", "2. Search for treasure", "3. Cross the river"],
    },
    3: {
        "option": "Mysterious encounters",
        "choices": ["1. Encounter a wizard", "2. Meet a friendly dragon"],
    },
    4: {
        "option": "Final challenges",
        "choices": ["1. Battle with a monster", "2. Solve a riddle"],
    },
}

def get_option_prompt(option_id: int) -> List[str]:
    """Returns prompt for the option based on option_id."""
    option = OPTIONS[option_id]["option"]
    choices = OPTIONS[option_id]["choices"]
    return [option] + choices + ["Enter your choice followed by the star sign."]

def confirm_option(option_id: int, user_choice: str) -> List[str]:
    """Confirm the user's selected option and return the appropriate response."""
    return [f"You have chosen to {user_choice}. Enjoy your adventure!"]

class JaxlIVRAdventureWebhook(BaseJaxlIVRWebhook):
    """Adventure.json webhook implementation."""

    def __init__(self) -> None:
        super().__init__()
        self._current_option_id: Optional[int] = None
        self._end_char = "*"

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "Adventure.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of adventure call")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        
        if "data" in request and request["data"] is not None:
            data = request["data"]
            assert data[-1] == self._end_char and self._current_option_id is not None
            
            if len(data) == 2 and data[0] == "0":
                self._current_option_id = None
                return MAIN_MENU
            
            user_choice = data[0]
            response_prompt = confirm_option(self._current_option_id, user_choice)
            return JaxlIVRResponse(
                prompt=response_prompt,
                num_characters=len(self._end_char),
                stream=None,
            )
        
        self._current_option_id = int(request["option"])
        return JaxlIVRResponse(
            prompt=get_option_prompt(self._current_option_id),
            num_characters=len(self._end_char),
            stream=None,
        )

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()

