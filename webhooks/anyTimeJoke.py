"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""
import random
from pathlib import Path
from typing import Any, Optional, Tuple

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)

JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "I told my wife she should embrace her mistakes. She gave me a hug.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
    "What do you call fake spaghetti? An impasta!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "I told my computer I needed a break and now it won't stop showing me vacation ads.",
    "Why did the math book look sad? It had too many problems.",
    "I'm on a seafood diet. I see food and I eat it.",
    "I would tell you a joke about an elevator, but it's an uplifting experience.",
    "Why do cows wear bells? Because their horns don't work.",
    "I'm trying to organize a hide and seek tournament, but good players are really hard to find.",
    "Did you hear about the mathematician who’s afraid of negative numbers? He’ll stop at nothing to avoid them.",
    "I used to be a baker, but I couldn’t make enough dough.",
    "Why did the scarecrow become a successful neurosurgeon? He was outstanding in his field.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "I told my computer I needed a break and now it won't stop showing me vacation ads.",
    "Why did the math book look sad? It had too many problems.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "I told my wife she should embrace her mistakes. She gave me a hug.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
    "What do you call fake spaghetti? An impasta!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "I told my computer I needed a break and now it won't stop showing me vacation ads.",
    "Why did the math book look sad? It had too many problems.",
    "I'm on a seafood diet. I see food and I eat it.",
    "I would tell you a joke about an elevator, but it's an uplifting experience.",
    "Why do cows wear bells? Because their horns don't work.",
    "I'm trying to organize a hide and seek tournament, but good players are really hard to find.",
    "Did you hear about the mathematician who’s afraid of negative numbers? He’ll stop at nothing to avoid them.",
    "I used to be a baker, but I couldn’t make enough dough.",
    "Why did the scarecrow become a successful neurosurgeon? He was outstanding in his field.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "I told my computer I needed a break and now it won't stop showing me vacation ads.",
    "Why did the math book look sad? It had too many problems.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "I told my wife she should embrace her mistakes. She gave me a hug.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
    "What do you call fake spaghetti? An impasta!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "I told my computer I needed a break and now it won't stop showing me vacation ads.",
    "Why did the math book look sad? It had too many problems.",
    "I'm on a seafood diet. I see food and I eat it.",
    "I would tell you a joke about an elevator, but it's an uplifting experience.",
    "Why do cows wear bells? Because their horns don't work.",
    "I'm trying to organize a hide and seek tournament, but good players are really hard to find.",
    "Did you hear about the mathematician who’s afraid of negative numbers? He’ll stop at nothing to avoid them.",
    "I used to be a baker, but I couldn’t make enough dough.",
    "Why did the scarecrow become a successful neurosurgeon? He was outstanding in his field.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "I told my computer I needed a break and now it won't stop showing me vacation ads.",
    "Why did the math book look sad? It had too many problems.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "I told my wife she should embrace her mistakes. She gave me a hug.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
    "What do you call fake spaghetti? An impasta!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "I told my computer I needed a break and now it won't stop showing me vacation ads.",
    "Why did the math book look sad? It had too many problems.",
    "I'm on a seafood diet. I see food and I eat it.",
    "I would tell you a joke about an elevator, but it's an uplifting experience.",
    "Why do cows wear bells? Because their horns don't work.",
    "I'm trying to organize a hide and seek tournament, but good players are really hard to find.",
    "Did you hear about the mathematician who’s afraid of negative numbers? He’ll stop at nothing to avoid them.",
    "I used to be a baker, but I couldn’t make enough dough.",
    "Why did the scarecrow become a successful neurosurgeon? He was outstanding in his field.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "I told my computer I needed a break and now it won't stop showing me vacation ads.",
    "Why did the math book look sad? It had too many problems.",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "I told my wife she should embrace her mistakes. She gave me a hug.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
    "What do you call fake spaghetti? An impasta!",
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "I told my computer I needed a break and now it won't stop showing me vacation ads.",
    "Why did the math book look sad? It had too many problems.",
    "I'm on a seafood diet. I see food and I eat it.",
    "I would tell you a joke about an elevator, but it's an uplifting experience.",
    "Why do cows wear bells? Because their horns don't work.",
    "I'm trying to organize a hide and seek tournament, but good players are really hard to find.",
    "Did you hear about the mathematician who’s afraid of negative numbers? He’ll stop at nothing to avoid them.",
    "I used to be a baker, but I couldn’t make enough dough.",
    "Why did the scarecrow become a successful neurosurgeon? He was outstanding in his field.",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "I used to play piano by ear, but now I use my hands.",
]

RETURN_PROMPT = [
    "Time to flip back to the main menu like a pancake on Sunday morning!",
    "Let's boomerang back to the main menu like a pro!",
    "Back to the main menu faster than a cat chasing a laser pointer!",
    "Returning to the main menu smoother than butter on hot toast!",
    "Main menu, here we come! Like a GPS rerouting a lost traveler.",
    "Back to the main menu like a rubber band snapping back into place!",
    "Returning to the main menu quicker than a hiccup!",
    "Main menu bound! Like a boomerang coming back to its thrower.",
    "Let's bounce back to the main menu like a kangaroo on springs!",
    "Time to main-menu-matic, just like magic!"
]

GOODBYE_MESSAGES = [
    "Thanks for joining the laughter club with Any Time Joke IVR! Until next time, keep those funny bones tickled! Goodbye!",
    "Catch you later, alligator! Thanks for laughing along with us.",
    "Adios amigos! Keep smiling and stay hilarious!",
    "Time to wrap up the jokes, but keep the laughter going wherever you go. Goodbye!",
    "Until we joke again! Thanks for dialing in for some laughs.",
    "Stay punny, my friend! See you next time around the joke block.",
    "Thanks for the giggles! Until next time, keep that sense of humor alive.",
    "So long and thanks for all the jokes! Goodbye with a chuckle.",
    "Time to sign off with a smile! Until our next laugh, take care!",
    "Auf Wiedersehen! Keep spreading the laughter wherever you go."
]

MAIN_MENU_PROMPT = [
    "Welcome! Get ready to laugh so hard, even your neighbors will wonder what's going on.",
    "Press 1 to hear a joke.",
    "Press 0 to exit."
]


MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

class JaxlIVRAnytimejokeWebhook(BaseJaxlIVRWebhook):
    """anyTimeJoke.json webhook implementation."""

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "anyTimeJoke.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of Call")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        option = request["option"]
        # Repeat menu scenario
        
        
        if option == "0":
            goodbye_msg = random.choice(GOODBYE_MESSAGES)
            return JaxlIVRResponse(prompt=[goodbye_msg], num_characters=1, stream=None)
        
        elif option == "1":
            joke = random.choice(JOKES)
            return JaxlIVRResponse(
                prompt=[f"Here's your joke: {joke}", "Press 1 to hear another joke.", "Press 2 to return to the main menu."],
                num_characters=1,
                stream=None
            )
        
        elif option == "2" :
            return_statement = random.choice(RETURN_PROMPT)
            return JaxlIVRResponse(
                prompt= [return_statement, "Press 1 to hear a joke.", "Press 0 to exit."],
                num_characters=1,
                stream=None,
            )
        
        else:
            return JaxlIVRResponse(
                prompt=["Invalid input! Invalid choice. Please try again.", "Press 1 to hear another joke.", "Press 2 to return to the main menu."],
                num_characters=1,
                stream=None
            )

    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        raise NotImplementedError()
