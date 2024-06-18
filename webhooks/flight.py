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
"Press 1 to book a flight. ",
"Press 2 to check flight details. ",
"Press 3 to manage your bookings. ",
"Press 0 followed by a star sign to repeat this menu",
]
MAIN_MENU = JaxlIVRResponse(
prompt=MAIN_MENU_PROMPT,
num_characters=1,
stream=None,
)
SERVICES = {
1: {
"service": "Book a flight",
"options": ["1. Domestic", "2. International"],
},
2: {
"service": "Check flight details",
"options": ["1. By flight number", "2. By departure time"],
},
3: {
"service": "Manage bookings",
"options": ["1. Cancel booking", "2. Reschedule booking"],
},
}
def get_service_prompt(service_id: int) -> List[str]:
"""Returns prompt for the service based on service_id."""
service = SERVICES[service_id]["service"]
options = SERVICES[service_id]["options"]
return [service] + options + ["Kindly enter the option number followed by the star sign."]
def confirm_service(service_id: int, user_answer: str) -> List[str]:
"""Get the user's selected option and return the appropriate response."""
return [f"Your service of {user_answer} has been confirmed"]
class JaxlIVRFlightWebhook(BaseJaxlIVRWebhook):
"""flight.json webhook implementation."""
def __init__(self) -> None:
super().__init__()
self._current_service_id: Optional[int] = None
self._end_char = "*"
@staticmethod
def config() -> ConfigPathOrDict:
return Path(__file__).parent.parent / "schemas" / "flight.json"
def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
    return MAIN_MENU
def teardown(self, request: JaxlIVRRequest) -> None:
print("End of call")
def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
assert request["option"]
if request.get("data", None) is not None:
data = request["data"]
assert data is not None
assert data[-1] == self._end_char and self._current_service_id is not None
if len(data) == 2 and data[0] == "0":
self._current_operation = None
return MAIN_MENU
user_answer = data[0]
response_prompt = confirm_service(self._current_service_id, user_answer)
return JaxlIVRResponse(
prompt=response_prompt,
num_characters=self._end_char,
stream=None,
)
self._current_service_id = int(request["option"])
return JaxlIVRResponse(
prompt=get_service_prompt(self._current_service_id),
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