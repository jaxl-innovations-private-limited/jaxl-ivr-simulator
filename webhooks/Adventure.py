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
    "Press 1 to visit the village.",
    "Press 2 to explore the forest.",
    "Press 3 to climb the mountain.",
    "Press 0 to repeat this menu.",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

def get_adventure_prompt(option: str) -> List[str]:
    """Returns prompt based upon user choice."""
    if option == "1":
        return [
            "You visit the village and meet a friendly villager.",
            "Press 1 to ask for directions.",
            "Press 2 to trade with the villager."
        ]
    elif option == "2":
        return [
            "You explore the forest and find a hidden path.",
            "Press 1 to follow the path.",
            "Press 2 to investigate the strange noise."
        ]
    elif option == "3":
        return [
            "You climb the mountain and reach a cave.",
            "Press 1 to enter the cave.",
            "Press 2 to set up camp outside the cave."
        ]
    elif option == "4":
        return [
            "You ask for directions and the villager points you to a nearby town.",
            "Press 1 to go to the town.",
            "Press 2 to stay in the village."
        ]
    elif option == "5":
        return [
            "You trade with the villager and get a magical item.",
            "Press 1 to use the item.",
            "Press 2 to keep it for later."
        ]
    elif option == "6":
        return [
            "You follow the path and find a river.",
            "Press 1 to drink the water.",
            "Press 2 to follow the river upstream."
        ]
    elif option == "7":
        return [
            "You investigate the noise and find a hidden treasure.",
            "Press 1 to take the treasure.",
            "Press 2 to leave it and continue exploring."
        ]
    elif option == "8":
        return [
            "You enter the cave and find ancient drawings.",
            "Press 1 to study the drawings.",
            "Press 2 to leave the cave."
        ]
    elif option == "9":
        return [
            "You set up camp and rest for the night.",
            "Press 1 to explore the surroundings.",
            "Press 2 to stay at the camp."
        ]
    else:
        return ["Invalid choice. Please try again."]

class JaxlIVRAdventureWebhook(BaseJaxlIVRWebhook):
    """Adventure game IVR webhook implementation."""

    def __init__(self) -> None:
        super().__init__()
        self._current_path: Optional[str] = None
        self._end_char = "*"
        self._separator = "#"

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "adventure.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        request["name"] = "adventure"  # Ensure the name is set to adventure
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of call")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        if request.get("data", None) is not None:
            data = request["data"]
            assert data is not None
            assert data[-1] == self._end_char and self._current_path
            if len(data) == 2 and data[0] == "0":
                self._current_path = None
                return MAIN_MENU

            option = data[0]
            next_path = f"{self._current_path}_{option}" if self._current_path else option
            prompt = get_adventure_prompt(next_path)
            self._current_path = next_path if prompt != ["Invalid choice. Please try again."] else self._current_path
            
            return JaxlIVRResponse(
                prompt=prompt,
                num_characters=1,
                stream=None
            )

        self._current_path = request["option"]
        return JaxlIVRResponse(
            prompt=get_adventure_prompt(request["option"]),
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
