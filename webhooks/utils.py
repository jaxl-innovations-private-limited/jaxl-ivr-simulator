
import razorpay
import os
import dotenv

dotenv.load_dotenv()
razorpay_key_id = os.getenv('RAZORPAY_KEY_ID')
razorpay_secret = os.getenv('RAZORPAY_SECRET')

def createPaymentLink(contact,amount):      #this function will sent payment link for reserving a seat

    try:
        client = razorpay.Client(auth=(razorpay_key_id, razorpay_secret))
        payment_Url = client.payment_link.create({
        "amount": amount,
        "currency": "INR",
        "accept_partial": True,
        "first_min_partial_amount": 100,
        "description": "For Seat Reservation",
        "customer": {
            "contact": contact
        },
        "notify": {
            "sms": True,
            "email": True
        },
        "reminder_enable": True,
        "callback_url": "https://example-callback-url.com/",
        "callback_method": "get"
        })
        return payment_Url
    except Exception as e:
        print("Exception ",e)
        return "Null"
    
# print(createPaymentLink("99999999",50000))