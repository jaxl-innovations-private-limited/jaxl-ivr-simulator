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

MAIN_MENU_PROMPT=[
    "wellcome to lite banking by jaxl",
    "Press 1 to check balance ",
    "Press 2 for transferring money",
    "Press 3 for last five transactions ",
    "Press 4 to block stolen card",
    "Press 0 followed by a star sign to repeat this menu",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

class JaxlIVRLitebankingWebhook(BaseJaxlIVRWebhook):
    """lite_Banking.json webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "lite_Banking.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of call")
        # return
        # raise NotImplementedError()

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        raise NotImplementedError()

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()
