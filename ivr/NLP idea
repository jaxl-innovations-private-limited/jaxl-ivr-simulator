
- More advanced NLP processing to handle complex customer inputs
- Audio playback and recording functionality
- Telephone interface integration (if using a physical phone line)


import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.intent import IntentClassifier
import sqlite3

# Initialize IVR system
ivr = pyttsx3.init()

# Connect to database
conn = sqlite3.connect("customer_data.db")
cursor = conn.cursor()

# Define product catalog
products = {
    "electronics": ["iPhone", "Samsung TV", "Sony Headphones"],
    "fashion": ["Nike Shoes", "Levi's Jeans", "Gucci Bag"]
}

# Define NLP model
nlp = IntentClassifier()

# Start IVR conversation
ivr.say("Welcome to our IVR system! How can I assist you today?")
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    audio = recognizer.record(source)
    text = recognizer.recognize_google(audio)
    tokens = word_tokenize(text)
    intent = nlp.classify(tokens)
    if intent == "product_query":
        ivr.say("What type of product are you looking for?")
        with sr.Microphone() as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            category = text.lower()
            if category in products:
                ivr.say("Great! Here are some recommendations:")
                for product in products[category]:
                    ivr.say(product)
            else:
                ivr.say("Sorry, we don't have that category.")
    elif intent == "order_placement":
        ivr.say("Which product would you like to order?")
        with sr.Microphone() as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            product = text.lower()
            place_order(product)
    elif intent == "customer_preference":
        ivr.say("What is your preference?")
        with sr.Microphone() as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            preference = text.lower()
            store_preference(cursor, preference)
    else:
        ivr.say("Sorry, I didn't understand that. Please try again.")

def place_order(product):
    cursor.execute("INSERT INTO orders (product) VALUES (?)", (product,))
    conn.commit()
    ivr.say(f"Okay, you have ordered {product}. Your order will be processed soon.")

def store_preference(cursor, preference):
    cursor.execute("INSERT INTO customer_preferences (preference) VALUES (?)", (preference,))
    conn.commit()
    ivr.say(f"Thank you for sharing your preference, {preference}!")

# Run the IVR system
ivr.run()

