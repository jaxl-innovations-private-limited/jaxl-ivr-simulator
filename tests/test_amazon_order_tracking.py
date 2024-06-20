"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

import unittest
from . import webhooks
track_order_stat = webhooks.amazon_order_tracking.track_order_status
get_order_status_mess = webhooks.amazon_order_tracking.get_order_status_message 
cancel_ord = webhooks.amazon_order_tracking.cancel_order

class TestAmazonOrderTracking(unittest.TestCase):
    def test_track_order_status(self):
        self.assertEqual(track_order_stat("1234567890"), "Your order is out for delivery")
        self.assertEqual(track_order_stat("0987654321"), "Your order has been shipped")
        self.assertEqual(track_order_stat("1112131415"), "Your order is being processed")
        self.assertEqual(track_order_stat("1615141312"), "Your order has been delivered")
        self.assertEqual(track_order_stat("1716151413"), "Your order has been cancelled")
        self.assertEqual(track_order_stat("0000000000"), "Order not found")

    def test_get_order_status_message(self):
        self.assertEqual(get_order_status_mess("Your order is out for delivery"), "Your order is on the way and should arrive soon.")
        self.assertEqual(get_order_status_mess("Your order has been shipped"), "Your order has been shipped and is on its way.")
        self.assertEqual(get_order_status_mess("Your order is being processed"), "Your order is currently being processed.")
        self.assertEqual(get_order_status_mess("Your order has been delivered"), "Your order has been delivered. We hope you enjoy your purchase!")
        self.assertEqual(get_order_status_mess("Your order has been cancelled"), "Your order has been cancelled. Please contact support for further assistance.")
        self.assertEqual(get_order_status_mess("Order not found"), "Order status not found.")

    def test_cancel_order(self):
        self.assertEqual(cancel_ord("1234567890"), "Your order has been successfully cancelled.")
        self.assertEqual(cancel_ord("0000000000"), "Order not found. Unable to cancel the order.")
        self.assertEqual(track_order_stat("1234567890"), "Your order has been cancelled")

if __name__ == "__main__":
    unittest.main()
