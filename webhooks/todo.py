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
    "Welcome to the To-Do List Manager.",
     " Press 1 to view task.",
      " Press 2 to add a tasks.",
       " Press 3 to delete a task.",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

to_do_list=["complete assignment of Jaxl","more explore about python"]
def get_operation_name(option: str) -> str:
    if option == "1":
        return "view_task"
    if option == "2":
        return "add"
    if option == "3":
        return "delete"
    raise NotImplementedError()


def get_operation_prompt(option: str) -> List[str]:
    if(option=="1"):
        if(len(to_do_list)>0):
            return [f"Your task is{to_do_list} all the best"]
        else:
            return ["You have no task!!!"

            ]
    elif(option=="3"):
        return [
            "your first task is going to delete, press 1 followed by * to confirm"
        ]
    
    else:
        return [
        f"Please write or tell about your task which you want to {get_operation_name(option)} followed by star,"
        ]
class JaxlIVRTodoWebhook(BaseJaxlIVRWebhook):
    """todo.json webhook implementation."""
    def __init__(self) -> None:
        super().__init__()
        self._current_operation: Optional[str] = None
        self._end_char = "*"
    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "todo.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of call")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        self._current_operation = request["option"]
        if request.get("data", None) is not None:
            data= request["data"]
            assert data is not None
            assert data[-1] == self._end_char
            if(self._current_operation=="2"):
                to_do_list.append(data)
                return JaxlIVRResponse(
                   prompt=[ f"your task is added successfully","see you later"],
                    num_characters=self._end_char,
                    stream=None,
                )
            elif(self._current_operation=="3"):
                if(len(to_do_list)>0):
                    Task=to_do_list[0]
                    to_do_list.pop(0)
                    return JaxlIVRResponse(
                       prompt=[ f"your data{Task}  is deleted successfully ","see you again"],
                        num_characters=self._end_char,
                        stream=None,
                    )
                else:
                    return JaxlIVRResponse(
                       prompt=[ "Your task list is empty"],
                        num_characters=self._end_char,
                        stream=None,
                    )
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
