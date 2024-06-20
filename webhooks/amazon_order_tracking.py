"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

import json

# Mock data for order statuses and cancellations
ORDER_STATUSES = {
    "1234567890": "Your order is out for delivery",
    "0987654321": "Your order has been shipped",
    "1112131415": "Your order is being processed",
    "1615141312": "Your order has been delivered",
    "1716151413": "Your order has been cancelled"
}

def track_order_status(order_number):
    """
    Retrieve the status of the given order number.
    """
    return ORDER_STATUSES.get(order_number, "Order not found")

def get_order_status_message(order_status):
    """
    Generate a message based on the order status.
    """
    if order_status == "Your order is out for delivery":
        return "Your order is on the way and should arrive soon."
    elif order_status == "Your order has been shipped":
        return "Your order has been shipped and is on its way."
    elif order_status == "Your order is being processed":
        return "Your order is currently being processed."
    elif order_status == "Your order has been delivered":
        return "Your order has been delivered. We hope you enjoy your purchase!"
    elif order_status == "Your order has been cancelled":
        return "Your order has been cancelled. Please contact support for further assistance."
    else:
        return "Order status not found."

def cancel_order(order_number):
    """
    Mock function to cancel an order.
    """
    if order_number in ORDER_STATUSES:
        ORDER_STATUSES[order_number] = "Your order has been cancelled"
        return "Your order has been successfully cancelled."
    else:
        return "Order not found. Unable to cancel the order."

def lambda_handler(event, context):
    """
    Main entry point for the webhook, processes the IVR state and input.
    """
    state = event.get("state")
    order_number = event.get("input", {}).get("order_number")
    selection = event.get("input", {}).get("selection")

    if state == "track_order":
        order_status = track_order_status(order_number)
        order_status_message = get_order_status_message(order_status)
        return {
            "state": "provide_status",
            "order_status": order_status,
            "order_status_message": order_status_message
        }
    elif state == "confirm_cancellation":
        cancellation_message = cancel_order(order_number)
        return {
            "state": "cancellation_status",
            "cancellation_message": cancellation_message
        }

    return {
        "state": "end",
        "message": "Invalid state"
    }

# Example usage of the lambda_handler function
if __name__ == "__main__":
    # Mock event for tracking an order
    event_track = {
        "state": "track_order",
        "input": {
            "order_number": "1234567890"
        }
    }
    context = {}
    result_track = lambda_handler(event_track, context)
    print(json.dumps(result_track, indent=4))

    # Mock event for cancelling an order
    event_cancel = {
        "state": "confirm_cancellation",
        "input": {
            "order_number": "0987654321"
        }
    }
    result_cancel = lambda_handler(event_cancel, context)
    print(json.dumps(result_cancel, indent=4))








# from pathlib import Path
# from typing import Any, Optional, Tuple

# from jaxl.ivr.frontend.base import (
#     BaseJaxlIVRWebhook,
#     ConfigPathOrDict,
#     JaxlIVRRequest,
#     JaxlIVRResponse,
# )


# class JaxlIVRCalculatorWebhook(BaseJaxlIVRWebhook):
#     """calculator.json webhook implementation."""

#     @staticmethod
#     def config() -> ConfigPathOrDict:
#         return Path(__file__).parent.parent / "schemas" / "calculator.json"

#     def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
#         raise NotImplementedError()

#     def teardown(self, request: JaxlIVRRequest) -> None:
#         raise NotImplementedError()

#     def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
#         raise NotImplementedError()

#     def stream(
#         self,
#         request: JaxlIVRRequest,
#         chunk_id: int,
#         sstate: Any,
#     ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
#         raise NotImplementedError()
