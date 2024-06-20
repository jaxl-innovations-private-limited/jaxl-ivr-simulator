from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)


MAIN_MENU_PROMPT = [
   " Hello,this is a reminder call.  Your order  with that product is scheduled for delivery by end of today.",

    "Press 1, if you are available to receive it today",
    "Press 2, if the delivery boy can leave the delivery at the door",
    "Press 3, if you want to reschedule for another day",
    "Press 4, to speak to our customer executive",
    "Press 0 to repeat the menu",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

SERVICES = {
    1: {
        "service": "To confirm you are available to pick the order today",
       
        "options": ["1.Yes, I'm available to take order in Morning Shift", "2. Yes, I'm available to take order onto Evening Shift "],

    },
    2: {
        "service":"The delivery boy will leave the package at your door.",
        "options": {
            1: "Confirm",
            2: "Cancel",
            },

    },
    3: {
        "service":"Our customer executive will call you to reschedule the delivery",
        "options": {
            1: "Confirm",
            2: "Cancel",
            },
    },
    4: {
        "service":"Our customer executive will call you shortly.",
        "options": {
            1: "Confirm",
            2: "Cancel",
            },
    }
    ,0: {
        "service": MAIN_MENU_PROMPT
    }

}


def get_service_prompt(service_id: int) -> List[str]:
    """Returns prompt for the service based on service_id."""
    service = SERVICES[service_id]["service"]
    options = SERVICES[service_id]["options"]
    return [service] + options + ["Kindly enter the option number followed by the star sign."]

def confirm_service(service_id: int, user_answer: str) -> List[str]:
    """Get the user's selected option and return the appropriate response."""

    return ["Your service of {user_answer} has been confirmed" ]


class JaxlIVRRemindersWebhook(BaseJaxlIVRWebhook):
    """Reminders.json webhook implementation."""

    def __init__(self) -> None:
        super().__init__()
        self._current_operation: Optional[str] = None
        self._end_char = "*"

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "Reminders.json"

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
                    f"{confirm_service(self._current_operation, numbers)}",
                ],
                num_characters=self._end_char,
                stream=None,
            )
        self._current_operation = request["option"]
        return JaxlIVRResponse(
            prompt=get_service_prompt(request["option"]),
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