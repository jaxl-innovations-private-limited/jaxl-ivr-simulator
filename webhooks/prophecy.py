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
    "Press 1 to continue. ",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

prophecies = [
    "You will have good luck and overcome many hardships.",
    "A pleasant surprise is waiting for you.",
    "Your hard work will soon pay off.",
    "You are stronger than you think.",
    "Happiness is around the corner.",
    "Adventure lies ahead.",
    "Good things come to those who wait.",
    "You will find success in whatever you do.",
    "Believe in yourself and you will succeed.",
    "A dream you have will come true.",
    "Your kindness will lead you to success.",
    "You will soon be rewarded for your efforts.",
    "Today is the day to make new friends.",
    "Your creativity will soon bring you fame.",
    "A thrilling time is in your immediate future.",
    "You will find joy in a surprise.",
    "Your charm and wit will charm everyone you meet.",
    "Fortune favors the brave.",
    "You are a person of culture."
]




def get_operation_prompt() -> List[str]:
    """Returns prompt to speek based upon user choice."""
    return [
        "Enter any number between 1 and 20 followed by *. ",
    ]

class JaxlIVRProphecyWebhook(BaseJaxlIVRWebhook):
    """prophecy.json webhook implementation."""

    def __init__(self) -> None:
        super().__init__()
        self._current_operation: Optional[str] = None
        self._end_char = "*"

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "prophecy.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of call")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        if request["data"] is not None:
            data = request["data"]
            assert data is not None
            assert data[-1] == self._end_char
            input = data[:-1]
            try:
                index=int(input)-1
                return JaxlIVRResponse(
                        prompt=[prophecies[index],],
                        num_characters=3,
                        stream=None,
                    )
            except ValueError:
                return JaxlIVRResponse(
                    prompt=["Invalid input"],
                    num_characters=3,
                    stream=None,
                )
        self._current_operation = request["option"]
        return JaxlIVRResponse(
            prompt=get_operation_prompt(),
            num_characters=self._end_char,
            stream=None,
        )
            

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()