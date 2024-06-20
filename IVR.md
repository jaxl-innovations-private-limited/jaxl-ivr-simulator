# Amazon Order Tracking IVR

## Overview

This IVR system allows users to track their Amazon orders by entering an order number. The system will provide the status of the order.

## States

1. **welcome**: Welcomes the user.
2. **get_order_number**: Asks the user to enter their order number.
3. **track_order**: Tracks the order status.
4. **provide_status**: Provides the order status to the user.
5. **end**: Ends the call.

## Mock Order Status

For the purpose of this IVR, we have a mock function that returns the order status for a given order number.

## Running the IVR

1. Create a Python virtual environment and install dependencies.
2. Use Docker to simulate the IVR flow.
3. Use the web simulator to test the IVR.

See the project README for detailed instructions.
