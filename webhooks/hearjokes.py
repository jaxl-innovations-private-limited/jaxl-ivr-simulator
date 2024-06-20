"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from pathlib import Path
from typing import Any, List, Optional, Tuple

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)


MAIN_MENU_PROMPT = [
    "Press 1 to continue. ",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

jokes = [
    "Why don’t scientists trust atoms? Because they make up everything! They tell each other, 'Don’t worry, we’ll stick together!' It’s all about the little things that hold us up!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised. It’s a fine line between a good joke and a great one. Sometimes you just have to raise an eyebrow!",
    "Why don’t skeletons fight each other? They don’t have the guts. Even in the afterlife, it’s all about sticking to your bones. When push comes to shove, they just fall apart!",
    "What do you call fake spaghetti? An impasta. It’s always trying to pasta itself off as the real deal. You can’t trust those noodles, they’re too saucy!",
    "Why did the scarecrow win an award? Because he was outstanding in his field. Day in and day out, he stood tall, showing unwavering dedication. That’s what it takes to be the best!",
    "I would avoid the sushi if I were you. It’s a little fishy. Sometimes you just have to roll with it, but when things smell off, it’s better to swim away!",
    "Want to hear a joke about construction? I’m still working on it. It’s a building process. You lay down the foundation, and then brick by brick, you create something that stands the test of time!",
    "Why don’t some couples go to the gym? Because some relationships don’t work out. It’s all about the weight of the matter and lifting each other up. Sometimes, the heavy lifting isn’t physical!",
    "What did one ocean say to the other ocean? Nothing, they just waved. It’s all in the ebb and flow. Sometimes, the best conversations are the ones where you just feel the connection!",
    "Why can’t your nose be 12 inches long? Because then it would be a foot. It’s all about keeping things in proportion. Too much of a good thing can become something else entirely!",
    "Why was the math book sad? Because it had too many problems. Every page was another challenge, but it’s all about finding the solution. Sometimes, you just have to add up the good moments!",
    "Why don’t eggs tell jokes? Because they might crack up. It’s all about keeping a shell of composure. When things get too scrambled, it’s hard to keep your sunny side up!",
    "What do you get when you cross a snowman and a vampire? Frostbite. It’s a chilling combination. When things get icy, you better hope you’ve got a warm heart to melt the tension!",
    "Why was the bicycle always tired? Because it was two-tired. It’s hard to keep up when you’re always spinning your wheels. Sometimes, you need to rest and get back on track!",
    "How do you organize a space party? You planet. It’s all about stellar planning and making sure everyone has a blast. When it’s out of this world, you know it’s going to be unforgettable!",
    "Why did the golfer bring an extra pair of pants? In case he got a hole in one. It’s all about being prepared. When you’re on the green, you need to be ready for anything!",
    "Why don’t programmers like nature? It has too many bugs. Every line of code is a potential pitfall. When you’re debugging, it’s all about squashing those little problems!",
    "Why did the tomato turn red? Because it saw the salad dressing. It’s all about being caught in the moment. When you’re blushing, sometimes it’s best to just relish the experience!",
    "What did the left eye say to the right eye? Between you and me, something smells. It’s all about perspective. When you’re looking at the world, sometimes the truth is right under your nose!",
    "Why did the coffee file a police report? It got mugged. It’s a tough world out there for a cup of joe. Sometimes, you just have to stay grounded and keep brewing!"
]




def get_operation_prompt() -> List[str]:
    """Returns prompt to speek based upon user choice."""
    return [
        "Enter any number between 1 and 20 followed by *. ",
    ]

class JaxlIVRHearjokesWebhook(BaseJaxlIVRWebhook):
    """hearjokes.json webhook implementation."""

    def __init__(self) -> None:
        super().__init__()
        self._current_operation: Optional[str] = None
        self._end_char = "*"

    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "hearjokes.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of call")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        if request["data"] is not None:
            data = request["data"]
            assert data is not None
            assert data[-1] == self._end_char
            input = data[:-1]
            try:
                index=int(input)-1
                return JaxlIVRResponse(
                        prompt=[jokes[index] + " hahaha. ",],
                        num_characters=3,
                        stream=None,
                    )
            except ValueError:
                return JaxlIVRResponse(
                    prompt=["Invalid input"],
                    num_characters=3,
                    stream=None,
                )
        self._current_operation = request["option"]
        return JaxlIVRResponse(
            prompt=get_operation_prompt(),
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