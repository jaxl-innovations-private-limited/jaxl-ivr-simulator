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




Booking_details = dict()        #to store details of user


STARTING_PROMPT = [
    "Welcome to XYZ Restaurant. ",
    "Press 1 to make a seat reservation. ",
    "Press 2 know, our location details. ",
    "Press 3 to speak with a customer service representative. ",
    "Press 4 for take away a dish. ",
    "Press 0 to repeat this menu. "
    ]

    

MAIN_MENU = JaxlIVRResponse(
    prompt=STARTING_PROMPT,
    num_characters=1,
    stream=None,
)
def get_custom_prompt(option: List[str]) -> JaxlIVRResponse:
    
    return JaxlIVRResponse(
        prompt = option,
        num_characters = "*",
        stream = None
    ) 

def checkdate(input:str) -> bool:
    try:

        if len(input)<=2:return False
        dates = input.split("#")
        if len(dates)!=2:
            return False
        day = int(dates[1])
        month = int(dates[0])
        print("\ndates = ",day," ",month)
        if month <= 0 or month > 12:
            return False
        if (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12) and day > 31 or day<=0:
            return False
        if (month == 2 or month == 4 or month == 6 or month == 9 or month == 11) and day > 30 or day<=0:
            return False
        return True
    except Exception as e:
        return False
def validTime(input:str) -> bool:
    try:

        if len(input)<=2:return False
        time = input.split("#")
        if len(time)!=2:return False
        hour = int(time[0])
        min = int(time[1])
        print("\ndates = ",hour," ",min)
        if hour<0 or hour>24 or min<0 or min>60:
            return False
        return True
    except Exception as e:
        return False

def bookingCompleted(input:str) -> bool:
    try:
        print(Booking_details,"\n")
        if input == "1":
            # from utils import createPaymentLink           #for sending payment link 
            # success = createPaymentLink(Booking_details.get("phone"),Booking_details.get("amt"+"00"))
            return True
        return False
    except Exception as e:
        return False

def calcAmout(input:str) -> int:
    if(input == "1"):
        return 120
    elif input == "2":
        return 40
    elif input == "3":
        return 60
    elif input == "4":
        return 30
    elif input == "5":
        return 20
    else:
        return 0

    


def send_link2(extra:str = "",deposit: int = 0) -> List[str]:
    prompt = [
        f"To secure your reservation, we need a deposit of {deposit}. Enter Your Phone Number for payment information .End with star sign. "
    ]
    return prompt

def get_date_prompt(extra:str = "") -> List[str]:
    prompt = [
        f"{extra}Please enter the date for your reservation in MMDD format, separated by hash. End with star Sign. like if you want to enter date of 12 January then enter Zero One Hash Twelve star. ",
        " Press 0, end with star, to repeat this. "
    ]
    return prompt

def get_food_items(extra:str="") -> List[str]:
    prompt = [
        f"{extra}Here is Our popular food items. ",
        " Press one for Frizzle Classic Veg, end with star. ",
        " Press two for Cheese corn sandwich, end with star. ",
        " Press three for red Sauce pasta, end with star. ",
        " Press four for Vanilla icecream, end with star. ",
        " press five for chocolates icecream, end with star. "
    ]
    return prompt

def get_time_prompt(extra:str = "") -> List[str]:
    prompt = [
        f"{extra}Please enter the time slots for your reservation in 24-hour format. separated by hash. End with star Sign. like if you want to enter time 12 30 then enter Twelve Hash Thirty star. ",
        " to repeat this Press 0, end with star. "
    ]
    return prompt


def get_party_size(option:str = "") -> List[str]:
    prompt = [
        f"{option}Please enter the number of people in your party. End with star Sign. ",
        " to repeat thisPress 0, end with star. "
    ]
    return prompt

def get_phone_num(option:str = "") -> List[str]:
    prompt = [
        f"{option}Please enter your contact number without any prefix. End with star sign. ",
        " to repeat thisPress 0, end with star. "
    ]
    return prompt

def send_link(deposit:int) -> List[str]:
    prompt = [
        f"To secure your reservation, we need a deposit of {deposit}. You will receive a payment link shortly on your entered phone number. Once payment is received, your order will be confirmed. press 1. To continue , press 2. to cancel the order.End with star sign "
    ]
    return prompt
    

def confirmation(date:str,time:str,party_size:str) -> List[str]:
    prompt = [
        f"You have selected a reservation for {date} at {time} for {party_size} people.",
        " Thanks for Choosing XYZ restraunt. ",
        " To confirm your seat please pay advance booking charges through link. "
    ]
    return prompt


def next_option(option:str,input: Optional[str] = "") -> Any:
    ans = dict()
    print("\nInput",input," option ",option)
    
    if option is None:
        ans["option"] = None
        ans["response"] = MAIN_MENU
    elif option == "Main1":
        ans["option"] = "get_date"
        ans["response"] = get_custom_prompt(get_date_prompt())
    
    elif option == "TakeAway":
        ans["option"] = "choose_items"
        ans["response"] = get_custom_prompt(get_food_items())
    
    elif option == "choose_items":
        amt = calcAmout(input)
        if amt != 0:
            ans["option"] = "takeAwayDetails"
            Booking_details["takeAwayAmt"] = amt
            ans["response"] = get_custom_prompt(send_link2("",amt))
        else:
            ans["option"] = "TakeAway"
            ans["response"] = get_custom_prompt(get_food_items("Wrong Input. "))
    elif option == "takeAwayDetails":
        if len(input)!=10:
            ans["option"] = "takeAwayDetails"
            ans["response"] = get_custom_prompt(send_link2("Wrong Input. ",Booking_details.get("takeAwayAmt")))
        else:
            Booking_details["takeAwayPhone"] = input
            ans["option"] = "takeAwayDetails2"
            ans["response"] = get_custom_prompt(["Enter time when you will be come for take away. time slots for your reservation in 24-hour format. separated by hash. End with star Sign. like if you want to enter time 12 30 then enter Twelve Hash Thirty star. "])
    elif option == "takeAwayDetails2":
        if not validTime(input):
            ans["option"] = "takeAwayDetails2"
            ans["response"] = get_custom_prompt(["Wrong INput. time slots for your reservation in 24-hour format. separated by hash. End with star Sign. like if you want to enter time 12 30 then enter Twelve Hash Thirty star. "])
        else:
            time = input.split("#")
            Booking_details["takeAwaytime"] = f"{time[0]} hour {time[1]} minute"
            ans["option"] = "stop"
            ans["response"] = get_custom_prompt(["Thanks for choosing our Restraunt.Please Pay your amount with the link to complete your order. "])


    elif option == "Main2":
        ans["option"] = "None"
        ans["response"] = get_custom_prompt(["Our Location is XYZ. Thank You. Enter Zero with end star to go to Main Menu. "])
    elif option == "Main3":
        ans["Option"] = "None"
        ans["response"] = get_custom_prompt(["Our Team Will Surely response you for your queries. Thank you. "])
    
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
            Booking_details["amt"] = totalMoney
            ans["option"] = "get_link"
            ans["response"] = get_custom_prompt(send_link(totalMoney))
    
    elif option == "get_link":
        if bookingCompleted(input):
            ans["option"] = "completed"
            ans["response"] = get_custom_prompt(confirmation(Booking_details.get("date"),Booking_details.get("time"),Booking_details.get("partySize")))
        else:
            ans["option"] = "stop"
            ans["response"] = get_custom_prompt([" Thanks for calling. "])
    
    elif option == "completed":
        if(input == "1"):
            ans["option"] = "stop"
            ans["response"] = get_custom_prompt(["Thanks you for choosing XYZ Restaurant. "])
        elif input == "2":
            ans["option"] = None
            ans["response"] = ["Thank You. "]

    else:
        ans["option"] = None
        ans["response"] = MAIN_MENU
    
    return ans


class JaxlIVRCalculatorWebhook(BaseJaxlIVRWebhook):
    """calculator.json webhook implementation."""

    def __init__(self) -> None:
        super().__init__()
        self.__current_option:Optional[str] = None
        self._end_char = "*"
        self.separtor = "#"
    
    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "myRestraunt.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        request.clear()
        print("end")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        option = request.get("option")
        data = str(request.get("data")).split("*")[0]
        print(f"Hey this is print \n-------------Your request{request} {data} {option}")
        if option == "0" and data == None:
            self.__current_option = None
            return MAIN_MENU
        elif (self.__current_option is None and option == '1'):
            self.__current_option = "Main1"
        elif self.__current_option is None and option == "2":
            self.__current_option = "Main2"
        elif self.__current_option is None and option == "3":
            self.__current_option = "Main3"
        elif self.__current_option is None and option == "4":
            self.__current_option = "TakeAway"
        elif self.__current_option == "stop":
            self.__current_option = None
            return JaxlIVRResponse(
                prompt = "",
                num_characters = 1,
                stream = None
            )
        print("\nSelf currenction optoin",self.__current_option)
        query = next_option(self.__current_option,data)
        print("This Is Query = ",query,"\n")
        print("\nOption = ",option)
        self.__current_option = query.get("option")
        return query.get("response")
        

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()

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
    #   getcall
    # MAIN_MENU4(TakeAway)
    #   Choose item
    #   enter phone number
    #   enter time slot