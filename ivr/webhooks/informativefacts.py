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

MAIN_MENU_PROMPT = [
    "Welcome! Please choose an option to listen some informative facts",
    "Press 1 for facts about humans.",
    "Press 2 for facts about animals.",
    "Press 3 for facts about insects.",
    "Press 4 for facts about plants",
    "Press 0 to repeat this menu again.",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

OPERATION_PROMPTS = {
    "1": ["The human heart beats more than three billion times in an average lifespan."],
    "2": ["Octopuses possess not one, not two, but three hearts! Two hearts pump blood to their gills, while the third pumps it to the rest of the body."],
    "3": ["Ants can lift and carry more than fifty times their own weight."],
    "4": [" Bamboo is the fastest-growing woody plant in the world. It can grow up to thirtyfive inches in a single day."],
}

INVALID_OPTION_PROMPT = [
    "Invalid input! Invalid choice. Please try again.",
    "Press 1 for facts about humans.",
    "Press 2 for facts about animals.",
    "Press 3 for facts about insects.",
    "Press 4 for facts about plants",
    "Press 0 to repeat this menu.",
]

def get_operation_prompt(option: str) -> list[str]:
    return OPERATION_PROMPTS.get(option, INVALID_OPTION_PROMPT)

class JaxlIVRInformativefactsWebhook(BaseJaxlIVRWebhook):
    """informativefacts.json webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "informativefacts.json"

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


# class JaxlIVRInformativefactsWebhook(BaseJaxlIVRWebhook):
#     """informativefacts.json webhook implementation."""

#     @staticmethod
#     def config() -> ConfigPathOrDict:
#         return Path(__file__).parent.parent / "schemas" / "informativefacts.json"

#     def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
#         raise NotImplementedError()

#     def teardown(self, request: JaxlIVRRequest) -> None:
#         raise NotImplementedError()

#     def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
#         raise NotImplementedError()

#     def stream(
#         self,
#         request: JaxlIVRRequest,
#         chunk_id: int,
#         sstate: Any,
#     ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
#         raise NotImplementedError()
