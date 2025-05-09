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

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)


def get_operation_name(option: str) -> str:
    """Returns operation name based upon user choice."""
    if option == "1":
        return "add"
    if option == "2":
        return "subtract"
    if option == "3":
        return "multiply"
    if option == "4":
        return "divide"
    raise NotImplementedError()


def get_operation_prompt(option: str) -> List[str]:
    """Returns prompt to speek based upon user choice."""
    return [
        f"Please enter numbers to {get_operation_name(option)} "
        + "separated by hash. End with star sign."
    ]


def calculate(option: str, numbers: List[int]) -> Union[int, float]:
    """Actual calculator that applies operation based upon passed option to numbers."""
    answer: Union[int, float]
    if option == "1":
        answer = sum(numbers)
    elif option == "2":
        answer = numbers[0]
        for number in numbers[1:]:
            answer = answer - number
    elif option == "3":
        answer = numbers[0]
        for number in numbers[1:]:
            answer = answer * number
    elif option == "4":
        answer = numbers[0]
        for number in numbers[1:]:
            answer = answer / number
    else:
        raise NotImplementedError()
    return answer


class JaxlIVRCalculatorWebhook(BaseJaxlIVRWebhook):
    """calculator.json webhook implementation."""

    def __init__(self) -> None:
        super().__init__()
        self._current_operation: Optional[str] = None
        self._end_char = "*"
        self._separator = "#"

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "calculator.json"

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
                return MAIN_MENU
            numbers = []
            for num in data[:-1].split(self._separator):
                try:
                    num = num.strip()
                    if num == "":
                        continue
                    numbers.append(int(num.strip()))
                except ValueError:
                    return JaxlIVRResponse(
                        prompt=["Invalid input. Please try again."],
                        num_characters=self._end_char,
                        stream=None,
                    )
            return JaxlIVRResponse(
                prompt=[
                    "The answer is",
                    f"{calculate(self._current_operation, numbers)}",
                ],
                num_characters=self._end_char,
                stream=None,
            )
        self._current_operation = request["option"]
        return JaxlIVRResponse(
            prompt=get_operation_prompt(request["option"]),
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
