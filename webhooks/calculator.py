# """
# Copyright (c) 2010-present by Jaxl Innovations Private Limited.

# All rights reserved.

# Redistribution and use in source and binary forms,
# with or without modification, is strictly prohibited.
# """

from pathlib import Path
import random
from typing import Any,List, Optional, Tuple

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)

STARTING_PROMPT = [
    "Welcome to our Online Payment Service. ",
    "Press 1 to make an Online Transaction Using UPI. ",
    "Press 2 to Check your Balance. ",
    "Press 3 to speak with a customer service representative. ",
    "Press 0 followed by the star key to repeat this menu. "
]

MAIN_MENU = JaxlIVRResponse(
    prompt=STARTING_PROMPT,
    num_characters=1,
    stream=None,
)

def get_custom_prompt(option: str) -> List[str]:
    """Returns prompt to speek based upon user choice."""
    return [
        f"You Have Pressed {option}. "
    ]
def get_Balance(upiId:str) -> int:
    return random.randint(100,10000)

def get_customer_upi(mobNumber:str) -> str:
    return f"{mobNumber}@{str(random.randint(3,7))}"

def get_customer_Balance(mobNumber:str) -> List[str]:
    upiID = get_cutomer_upiID(mobNumber)
    
    return [
        f"Your Balance is {get_Balance(upiID)}. "
    ]
    

class JaxlIVRCalculatorWebhook(BaseJaxlIVRWebhook):
    """calculator.json webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "calculator.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("Hey This TearDown")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        data = request.get("option")
        
        return JaxlIVRResponse(
            prompt=get_custom_prompt(str(data)),
            num_characters=1,
            stream=None,
        )

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:

        total_seconds = 10  # Example countdown from 10 seconds
        countdown = total_seconds - chunk_id
        if countdown > 0:
            return (sstate, JaxlIVRResponse(
                prompt=[f"Countdown: {countdown} seconds remaining"],
                num_characters=1,
                stream=1.0  # Stream again after 1 second
            ))
        else:
            return (sstate, JaxlIVRResponse(
                prompt=["Countdown complete!"],
                num_characters=1,
                stream=None  # End the stream
            ))
        raise NotImplementedError()

# Example usage (would be part of your IVR framework initialization code):
# ivr = JaxlIVRCalculatorWebhook()
# response = ivr.setup({"call_id": 12345})
# print(response)
