# """
# Copyright (c) 2010-present by Jaxl Innovations Private Limited.

# All rights reserved.

# Redistribution and use in source and binary forms,
# with or without modification, is strictly prohibited.
# """

from pathlib import Path
import random
from typing import Any,List,Dict, Optional, Tuple
# import razorpay

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
    )




Booking_details = dict()


STARTING_PROMPT = [
    "Welcome to XYZ Restaurant. ",
    "Press 1 to make a seat reservation. ",
    "Press 2 for location details. ",
    "Press 3 to speak with a customer service representative. ",
    "Press 4 to End this call. ",
    "Press 0 to repeat this menu. "
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
# def createPaymentLink():

    client = razorpay.Client(auth=("rzp_test_jSWmY7zG0itz74", "I4pTXYKpYip17Lu4hrGd2Gjf"))

    payment_Url = client.payment_link.create({
        "upi_link": true,
        "amount": 500,
        "currency": "INR",
        "accept_partial": false,
        "first_min_partial_amount": 100,
        "description": "For XYZ purpose",
        "customer": {
            "name": "Gaurav Kumar",
            "email": "gaurav.kumar@example.com",
            "contact": "+919000090000"
        },
        "notify": {
            "sms": true,
            "email": true
        },
        "reminder_enable": true,
        "notes": {
            "policy_name": "Jeevan Bima"
        }
    })
    return payment_Url
def checkdate(input:str) -> bool:
    dates = input.split("#")
    day = int(dates[0])
    month = int(dates[1])
    print("\ndates = ",day," ",month)
    if month <= 0 or month > 12:
        return False
    if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12) and day > 31 or day<=0:
        return False
    if (month == 2 or month == 4 or month == 6 or month == 9 or month == 11) and day > 30 or day<=0:
        return False
        
    return True
def validTime(input:str) -> bool:
    time = input.split("#")
    hour = int(time[0])
    min = int(time[1])
    print("\ndates = ",hour," ",min)
    if hour<0 or hour>24 or min<0 or min>60:
        return False
    return True

def bookingCompleted(input:str) -> bool:
    print(Booking_details,"\n")
    if input == "1":
        return True
    return False

def next_option(option:str,input: Optional[str] = "") -> Any:    #fix this return type
    ans = dict()
    print("\nInput",input)
    if option == None:
        ans["option"] = "Main1"
        ans["response"] = MAIN_MENU
    
    if option == "Main1":
        ans["option"] = "get_date"
        ans["response"] = get_custom_prompt(get_date_prompt())
    
    elif option == "Main2":
        ans["option"] = None
        ans["response"] = get_custom_prompt(["Our Restraunt Location is XYZ. Thank You. Enter Any key with end * to go to Main Menu. "])
    elif option == "Main3":
        # print("Payment Link = ",createPaymentLink())
        ans["Option"] = None
        ans["response"] = get_custom_prompt(["Our Team Will Surely response for your queries. Thank you. "])
    
    elif option == "Main4":
        ans["option"] = "stop"
        ans["response"] = get_custom_prompt(["Thanks for Calling. "])
    
    elif option == "get_date":
        dates = input.split("#")
        if (input == "0"):
            print("Inside 0 Option")
            ans["option"] = "get_date"
            ans["response"] = get_custom_prompt(get_date_prompt())
        elif(not checkdate(input)):
            ans["option"] = "get_date"
            ans["response"] = get_custom_prompt(get_date_prompt("Invalid Input. "))
        else:
            Booking_details["date"] = f"{dates[0]} {dates[1]}"
            ans["option"] = "get_time"
            ans["response"] = get_custom_prompt(get_time_prompt())

    elif option == "get_time":
        if (input == "0"):
            ans["option"] = "get_time"
            ans["response"] = get_custom_prompt(get_time_prompt())
        elif not validTime(input):
            ans["option"] = "get_time"
            ans["response"] = get_custom_prompt(get_time_prompt("Invalid Input. "))
        else:
            time = input.split("#")
            Booking_details["time"] = f"{time[0]} hour {time[1]} minute"
            ans["option"] = "get_phone"
            ans["response"] = get_custom_prompt(get_phone_num())

    elif option == "get_phone":
        if (input == "0"):
            ans["option"] = "get_phone"
            ans["response"] = get_custom_prompt(get_phone_num())
        elif len(input) != 10:
            ans["option"] = "get_phone"
            print("Phone Number",input)
            ans["response"] = get_custom_prompt(get_phone_num("Invalid Input. "))
        else:
            Booking_details["phone"] = input
            ans["option"] = "get_size"
            ans["response"] = get_custom_prompt(get_party_size())
    elif option == "get_size":
        if (input == "0"):
            ans["option"] = "get_size"
            ans["response"] = get_custom_prompt(get_party_size())
        elif not input.isdigit():
            ans["option"] = "get_size"
            ans["response"] = get_custom_prompt(get_party_size("Invalid Input. "))
        else:
            party_size = int(input)
            Booking_details["partySize"] = input
            totalMoney = 100*party_size
            ans["option"] = "get_link"
            ans["response"] = get_custom_prompt(send_link(totalMoney))
    
    elif option == "get_link":
        if bookingCompleted("1"):
            ans["option"] = "completed"
            ans["response"] = get_custom_prompt(confirmation(Booking_details.get("date"),Booking_details.get("time"),Booking_details.get("partySize")))
        else:
            ans["option"] = None
            ans["response"] = MAIN_MENU
    
    elif option == "completed":
        if(input == "1"):
            ans["option"] = "stop"
            ans["response"] = get_custom_prompt(["Thanks you for choosing XYZ Restaurant. "])
        elif input == "2":
            ans["option"] = None
            ans["response"] = MAIN_MENU

    else:
        ans["option"] = None
        ans["response"] = MAIN_MENU
    
    return ans
        
    




def get_date_prompt(extra:str = "") -> List[str]:
    prompt = [
        f"{extra}Please enter the date for your reservation in MMDD format, separated by hash. End with star Sign. like if you want to enter date of 12 January then enter Zero One Hash Twelve star. ",
        " Press 0, end with star, to repeat this. "
    ]
    return prompt

def get_time_prompt(extra:str = "") -> List[str]:
    prompt = [
        f"{extra}Please enter the time slots for your reservation in 24-hour format. separated by hash. End with star Sign. like if you want to enter time 12 30 then enter Twelve Hash Thirty star. ",
        " Press 0, end with star, to repeat this. "

    ]
    return prompt


def get_party_size(option:str = "") -> List[str]:
    prompt = [
        f"{option}Please enter the number of people in your party. End with star Sign. ",
        "Press 0, end with star, to repeat this. "
    ]
    return prompt

def get_phone_num(option:str = "") -> List[str]:
    prompt = [
        f"{option}Please enter your contact number without any prefix. End with star sign. ",
        "Press 0, end with star, to repeat this. "
    ]
    return prompt

def send_link(deposit:int) -> List[str]:
    prompt = [
        f"To secure your reservation, we need a deposit of {deposit}. You will receive a payment link shortly on your entered phone number. Once payment is received, your reservation will be confirmed. press 1. To continue , press 2. to start over.End with star sign "
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

    def __init__(self) -> None:
        super().__init__()
        self.__current_option:Optional[str] = None
        self._end_char = "*"
        self.separtor = "#"
    
    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "calculator.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        request.clear()
        print("end")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        option = request.get("option")
        data = str(request.get("data")).split("*")[0]
        print(f"Hey this is print \n-------------Your request{request}")
        if (self.__current_option == None and option == "1"):
            self.__current_option = "Main1"
        elif self.__current_option == None and option == "2":
            self.__current_option = "Main2"
        elif self.__current_option == None and option == "3":
            self.__current_option = "Main3"
        elif self.__current_option == None and option == "4":
            self.__current_option = "Main4"
        elif self.__current_option == "stop":
            self.teardown(request)
            self.__current_option = None
            return JaxlIVRResponse(
                prompt = "",
                num_characters = 1,
                stream = None
            )
        query = next_option(self.__current_option,data)
        print("This Is Query = ",query,"\n")
        self.__current_option = query.get("option")
        return query.get("response")
        

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
