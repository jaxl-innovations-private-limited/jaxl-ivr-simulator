"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from pathlib import Path
from typing import Any, Optional, Tuple

from . import banking
import random

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)

MAIN_MENU_PROMPT=[
    "wellcome to lite banking by jaxl",
    "Press 1 to check balance ",
    "Press 2 for transferring money",
    "Press 3 for last five transactions ",
    "Press 4 to block stolen card",
    "press 9 to repeat this menu",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

class JaxlIVRLitebankingWebhook(BaseJaxlIVRWebhook):
    """lite_Banking.json webhook implementation."""

    def __init__(self) -> None:
        super().__init__()
        self.current_state: Optional[str] = None
        self._end_char = "*"
        self._separator = "#"
        self.acc=banking.account(random.randint(111111,999999))


    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "lite_Banking.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        self.current_state="main_menu"
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of call")
        # return
        # raise NotImplementedError()

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        return  
        # if request.get("data", None) is not None:
        #     data = request["data"]
        #     assert data is not None
        #     assert data[-1] == self._end_char and self.current_state
        #     # Repeat menu scenario
        #     if len(data) == 2 and data[0] == "0":
        #         self.current_state = None
        #         return MAIN_MENU
        #     numbers = []
        #     for num in data[:-1].split(self._separator):
        #         try:
        #             num = num.strip()
        #             if num == "":
        #                 continue
        #             numbers.append(int(num.strip()))
        #         except ValueError:
        #             return JaxlIVRResponse(
        #                 prompt=["Invalid input. Please try again."],
        #                 num_characters=self._end_char,
        #                 stream=None,
        #             )
        #     return JaxlIVRResponse(
        #         prompt=[
        #             "The answer is",
        #             f"{calculate(self.current_state, numbers)}",
        #         ],
        #         num_characters=self._end_char,
        #         stream=None,
        #     )
        # self.current_state = request["option"]
        # return JaxlIVRResponse(
        #     prompt=get_operation_prompt(request["option"]),
        #     num_characters=self._end_char,
        #     stream=None,
        # )

        # print('\n'*5)
        # for i in request:
        #     print(i,request[i])
        # print('\n'*5)
        # return JaxlIVRResponse(
        #     prompt=["press any thing"],
        #     num_characters=5,
        #     stream=None,
        # )

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()
