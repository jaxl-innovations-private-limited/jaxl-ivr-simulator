# """
# Copyright (c) 2010-present by Jaxl Innovations Private Limited.

# All rights reserved.

# Redistribution and use in source and binary forms,
# with or without modification, is strictly prohibited.
# """

from pathlib import Path
import random
from typing import Any,List,Dict, Optional, Tuple

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
    )




# Booking_details = dict()

STARTING_PROMPT = [
    "Welcome to XYZ Restaurant. ",
    "Press 1 to make a seat reservation. ",
    "Press 2 for location details. ",
    "Press 3 to speak with a customer service representative. ",
    "Press 0 followed by the star key to repeat this menu. "
    ]

    

MAIN_MENU = JaxlIVRResponse(
    prompt=STARTING_PROMPT,
    num_characters=1,
    stream=None,
)
def get_custom_prompt(option: List[str]) -> JaxlIVRResponse:
    """Returns prompt to speek based upon user choice."""
    
    return JaxlIVRResponse(
        prompt = option,
        num_characters = "*",
        stream = None
    ) 

def checkdate(input:str) -> bool:
    dates = input.split("#")
    day = int(dates[0])
    month = int(dates[1])
    
    if month <= 0 or month > 12:
        return False
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12 and day > 31:
        return False
    if day<=0 or month == 2 or month == 4 or month == 6 or month == 9 or month == 11 and day > 30:
        return False
        
        return True
def validTime(input:str) -> bool:
    time = input.split("#")
    hour = int(time[0])
    min = int(time[1])
    if hour<0 or hour>24 or min<0 or min>60:
        return False
    return True

def bookingCompleted() -> bool:
    return True

def next_option(option:str,input: Optional[str]) -> Any:    #fix this return type
    ans = dict()
    if option == "None":
        ans["option"] = "Main1"
        ans["response"] = MAIN_MENU
    
    if option == "Main1":
        ans["option"] = "get_date"
        ans["response"] = get_custom_prompt(get_date_prompt())
    
    elif option == "Main2":
        ans["option"] = "None"
        ans["response"] = get_custom_prompt(["Our Restraunt Location is XYZ. Thank You. "])
    elif option == "Main3":
        ans["Option"] = "None"
        ans["response"] = get_custom_prompt(["Our Team Will Surely resonse your queries. Thank you. "])
    elif option == "get_date":
        dates = input.split("#")
        if(not checkdate(input)):
            ans["option"] = "get_date"
            ans["response"] = get_custom_prompt(get_date_prompt("Invalid Input. "))
        else:
            Booking_details["date"] = input
            ans["option"] = "get_time"
            ans["response"] = get_custom_prompt(get_time_prompt())

    elif option == "get_time":
        if not validTime(input):
            ans["option"] = "get_time"
            ans["response"] = get_custom_prompt(get_time_prompt("Invalid Input. "))
        else:
            Booking_details["time"] = input
            ans["option"] = "get_phone"
            ans["response"] = get_custom_prompt(get_phone_num())

    elif option == "get_phone":
        if len(input)<10 or len(input)>10:
            ans["option"] = "get_phone"
            ans["response"] = get_custom_prompt(get_phone_num("Invalid Input. "))
        else:
            Booking_details["phone"] = input
            ans["option"] = "get_size"
            ans["response"] = get_custom_prompt(get_party_size())
    elif option == "get_size":
        if not input.isdigit():
            ans["option"] = "get_size"
            ans["response"] = get_custom_prompt(get_party_size("Invalid Input. "))
        else:
            party_size = int(input)
            Booking_details["partySize"] = input
            totalMoney = 100*party_size
            ans["option"] = "get_link"
            ans["response"] = get_custom_prompt(send_link(totalMoney))
    
    elif option == "get_link":
        if bookingCompleted():
            ans["option"] = "completed"
            ans["response"] = get_custom_prompt(confirmation(Booking_details.get("date"),Booking_details.get("time"),Booking_details("partySize")))
    
    else:
        ans["option"] = "None"
        ans["response"] = MAIN_MENU
    
    return ans
        
    




def get_date_prompt(extra:str = "") -> List[str]:
    prompt = [
        f"{extra} Please enter the date for your reservation in MMDD format, separated by hash. End with star Sign. "
    ]
    return prompt

def get_time_prompt(extra:str = "") -> List[str]:
    prompt = [
        f"{extra} Please enter the time slots for your reservation in 24-hour format. separated by hash. End with star Sign. "
    ]
    return prompt


def get_party_size(option:str = "") -> List[str]:
    prompt = [
        f"{option}Please enter the number of people in your party. End with star Sign. "
    ]
    return prompt

def get_phone_num(option:str = "") -> List[str]:
    prompt = [
        f"{option}Please enter your contact number. End with star sign. "
    ]
    return prompt

def send_link(deposit:int) -> List[str]:
    prompt = [
        f"To secure your reservation, we need a deposit of {deposit}. You will receive a payment link shortly. Once payment is received, your reservation will be confirmed. press 1. To continue , press 2. to start over.End with star sign "
    ]
    return prompt
    

def confirmation(date:str,time:str,party_size:str) -> List[str]:
    prompt = [
        f"You have selected a reservation for {date} at {time} for {party_size} people. To confirm, press 1.and To start over, press 2. End with star sign. "
    ]
    return prompt
   

# None
    # MAIN_MENU1
    #     get_date_prompt
    #     get_time_prompt
    #     get_phone_num
    #     get_party_size
    #     payment_link
    #     confirmation
    # MAIN_MENU2
    #     GetLocation
    # MAIN_MENU3
    #   call
    # MAIN_MENU4

class JaxlIVRCalculatorWebhook(BaseJaxlIVRWebhook):
    """calculator.json webhook implementation."""

    # def __init__(self) -> None:
    #     super().__init__()
    #     self.__current_option:Optional[str] = None
    #     self._end_char = "*"
    #     self.separtor = "#"
    
    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "calculator.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("Hey This TearDown")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        # data = request.get("option")
        # print(f"Hey this is print \n-------------Your request{request}")
        # if request.get("data") != None:
        #     if len(data)>1 and data[0] == "0" and data[1] == "*":
        #         return MAIN_MENU
        #     else:
        #         query = next_option(self.__current_option,data)
        #         # self.__current_option = query.get("option")
        #         return query.get("response")
        # else:
        #     query = next_option("None")
            # self.__current_option = query.get("option")
            # print(query)
        return JaxlIVRResponse(
            prompt = [
                "Hey this is working"
            ],
            num_characters="*",
            stream = None
        )
        
        

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()

# Example usage (would be part of your IVR framework initialization code):
# ivr = JaxlIVRCalculatorWebhook()
# response = ivr.setup({"call_id": 12345})
# print(response)
