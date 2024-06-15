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


class JaxlIVRCalculatorWebhook(BaseJaxlIVRWebhook):
    """calculator.json webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "calculator.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        raise NotImplementedError()

    def teardown(self, request: JaxlIVRRequest) -> None:
        raise NotImplementedError()

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        raise NotImplementedError()

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()
