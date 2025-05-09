"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from pathlib import Path
from typing import Any, Optional, Tuple
import logging

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)

class JaxlIVRQueryresolverWebhook(BaseJaxlIVRWebhook):
    """query_resolver.json webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "query_resolver.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        prompt = (
            "Welcome to the smartphone troubleshooting system. "
            "Press 1 for network issues, 2 for speaker issues, "
            "3 for battery issues, 4 for app issues, "
            "5 for system settings."
        )
        return JaxlIVRResponse(prompt=prompt, next_state="handle_option")

    def teardown(self, request: JaxlIVRRequest) -> None:
        logging.info("Teardown: Cleaning up resources for request ID %s", request.request_id)

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        user_input = request.dtmf
        if user_input == '1':
            return self.network_issue(request)
        elif user_input == '2':
            return self.speaker_issue(request)
        elif user_input == '3':
            return self.battery_issue(request)
        elif user_input == '4':
            return self.app_issue(request)
        elif user_input == '5':
            return self.system_setting(request)
        else:
            prompt = (
                "Invalid selection. Press 1 for network issues, "
                "2 for speaker issues, 3 for battery issues, "
                "4 for app issues, 5 for system settings."
            )
            return JaxlIVRResponse(prompt=prompt, next_state="handle_option")

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        return None

    def network_issue(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        prompt = "We are diagnosing your network issue. Please hold on."
        logging.info("Network issue selected for request ID %s", request.request_id)
        # Simulate diagnostics and offer solutions
        solutions = (
            "1. Restart your phone. ",
            "2. Check if Airplane mode is off. ",
            "3. Ensure mobile data or Wi-Fi is turned on. ",
            "4. Move to an area with better signal. ",
            "5. Contact your service provider."
        )
        prompt += " ".join(solutions)
        return JaxlIVRResponse(prompt=prompt, next_state="end")

    def speaker_issue(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        prompt = "We are diagnosing your speaker issue. Please hold on."
        logging.info("Speaker issue selected for request ID %s", request.request_id)
        # Simulate diagnostics and offer solutions
        solutions = (
            "1. Increase the volume. ",
            "2. Check if Do Not Disturb mode is on. ",
            "3. Restart your phone. ",
            "4. Clean the speaker grille. ",
            "5. Contact support if issue persists."
        )
        prompt += " ".join(solutions)
        return JaxlIVRResponse(prompt=prompt, next_state="end")

    def battery_issue(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        prompt = "We are diagnosing your battery issue. Please hold on."
        logging.info("Battery issue selected for request ID %s", request.request_id)
        # Simulate diagnostics and offer solutions
        solutions = (
            "1. Reduce screen brightness. ",
            "2. Close background apps. ",
            "3. Disable location services. ",
            "4. Check for battery-draining apps. ",
            "5. Replace battery if it’s old."
        )
        prompt += " ".join(solutions)
        return JaxlIVRResponse(prompt=prompt, next_state="end")

    def app_issue(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        prompt = "We are diagnosing your app issue. Please hold on."
        logging.info("App issue selected for request ID %s", request.request_id)
        # Simulate diagnostics and offer solutions
        solutions = (
            "1. Restart the app. ",
            "2. Update the app. ",
            "3. Clear app cache and data. ",
            "4. Reinstall the app. ",
            "5. Check for device compatibility."
        )
        prompt += " ".join(solutions)
        return JaxlIVRResponse(prompt=prompt, next_state="end")

    def system_setting(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        prompt = "We are diagnosing your system setting issue. Please hold on."
        logging.info("System setting issue selected for request ID %s", request.request_id)
        # Simulate diagnostics and offer solutions
        solutions = (
            "1. Restore default settings. ",
            "2. Check for system updates. ",
            "3. Perform a factory reset. ",
            "4. Ensure sufficient storage space. ",
            "5. Contact support if issue persists."
        )
        prompt += " ".join(solutions)
        return JaxlIVRResponse(prompt=prompt, next_state="end")
