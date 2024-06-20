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


# Products currently available in mart
# these items, for now are static ,
# but with the help of database can be updated accordingly
PRODUCTS_AVAILABLE={
    "1":{
        "product_name":"Apsara Pencil",
        "price":5
    },
    "2":{
        "product_name":"Natraj Pencil",
        "price":5
    },
    "3":{
        "product_name":"Classmate Notebook 30 Pages",
        "price":20
    },
    "4":{
        "product_name":"Classmate Notebook 50 Pages",
        "price":40
    }
}

# variables to store cart information
CART={
    "items":[],
    "total_price":0
}

# main menu prompt .... opens up when client first hits the system
MAIN_MENU_PROMPT=[
    "Welcome to IVR Grocer, your convenient IVR-based grocery store!",
    "Each product in our store has a unique product number.",
    "Enter the product number followed by the * key to add the product to your cart.",
    "Press 0 followed by the * key to list all current items in your cart and the total amount.",
    "Press # followed by the * key to repeat this menu.",
]
MAIN_MENU=JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters="*",
    stream=None,
)

def validate_current_input(currentInput:str)->bool:
    if currentInput is None:
        return False
    elif len(currentInput)!=2:
        return False
    elif currentInput[1]!="*":
        return False
    elif currentInput[0]<"0" or currentInput[0]>"4":
        return False
    
    return True

def handle_input(currentInput:str)->list[str] :
    # Product details ..this could also be fetching from database 
    # return ["hey"]
    productId=currentInput[0]

    if(productId=="0"):
        items_in_cart=""
        for item in CART["items"]:
            items_in_cart=items_in_cart+" "+item
        return [
                "You have opted to view the contents of your cart:",
                f"Products currently in your cart are {items_in_cart}",
                f"Total amount {CART['total_price']} rupees",
                "To return to the main menu, please enter #*"
            ]
    choosenProduct=PRODUCTS_AVAILABLE[productId]
    
    if choosenProduct["product_name"] in CART["items"]:
        return ["Item Already in the Cart"]
    else:
        CART["items"].append(choosenProduct["product_name"])
        CART["total_price"]=CART["total_price"]+choosenProduct["price"]
        return [
                f"You have opted to add the product {choosenProduct['product_name']}.",
                f"{choosenProduct['product_name']} is priced {choosenProduct['price']} rupees.",
                f"Product {choosenProduct['product_name']} added successfully.",
                "To return to the main menu, please enter #*"
            ]
        

class JaxlIVRIvrgrocerWebhook(BaseJaxlIVRWebhook):
    """IVRGrocer.json webhook implementation."""
    def __init__(self) -> None:
        super().__init__()
        self._end_char = "*"

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "IVRGrocer.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print(f"You need to pay a total of {CART['total_price']}.")
        raise NotImplementedError()
    
    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        if request.get("data", None) is not None:
            data = request["data"]
            assert data is not None
            assert data[-1] == self._end_char
            # Repeat menu scenario
            if len(data) == 2 and data[0] == "#":
                return MAIN_MENU
            
            if validate_current_input(data)==False:
                return JaxlIVRResponse(
                    prompt=["Please check your input again."],
                    num_characters=self._end_char,
                    stream=None
                )
            result=handle_input(data)
            return JaxlIVRResponse(
                prompt=result,
                num_characters=self._end_char,
                stream=None,
            )
        return JaxlIVRResponse(
            prompt=MAIN_MENU_PROMPT,
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
