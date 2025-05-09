"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

from jaxl.ivr.frontend.base import (
    BaseJaxlIVRWebhook,
    ConfigPathOrDict,
    JaxlIVRRequest,
    JaxlIVRResponse,
)


MAIN_MENU_PROMPT = [
    "Press 1 for the first question. ",
    "Press 2 for the second question. ",
    "Press 3 for the third question. ",
    "Press 4 for the fourth question. ",
    "Press 0 followed by a star sign to repeat this menu",
]

MAIN_MENU = JaxlIVRResponse(
    prompt=MAIN_MENU_PROMPT,
    num_characters=1,
    stream=None,
)

QUESTIONS = {
    1: {
        "question": "What is the capital of France?",
        "options": ["1. Berlin", "2. Paris", "3. Madrid", "4. Rome"],
        "answer": "2",
    },
    2: {
        "question": "Which planet is known as the Red Planet?",
        "options": ["1. Earth", "2. Venus", "3. Mars", "4. Jupiter"],
        "answer": "3",
    },
    3: {
        "question": "Who wrote the novel 'Harry Potter and the Sorcerer's Stone'?",
        "options": ["1. J K Rowling", "2. Mark Twain", "3. Harper Lee", "4. Charles Dickens"],
        "answer": "1",
    },
    4: {
        "question": "Who is credited with inventing the modern steam engine?",
        "options": ["1. Thomas Edison", "2. Nikola Tesla", "3. James Watt", "4. Alexander Graham Bell"],
        "answer": "3",
    },
}

def get_question_prompt(question_id: int) -> List[str]:
    """Returns prompt for the question based on question_id."""
    question = QUESTIONS[question_id]["question"]
    options = QUESTIONS[question_id]["options"]
    return [question] + options + ["Please press the number corresponding to your answer followed by the star sign."]

def check_answer(question_id: int, user_answer: str) -> List[str]:
    """Checks the user's answer and returns the appropriate response."""
    correct_answer = QUESTIONS[question_id]["answer"]
    if user_answer == correct_answer:
        return ["Correct! You have won One crore rupees."]
    else:
        return ["Incorrect. The correct answer was " + str(correct_answer)]

class JaxlIVRKbcquizWebhook(BaseJaxlIVRWebhook):
    """kbc_quiz.json webhook implementation."""

    def __init__(self) -> None:
        super().__init__()
        self._current_question_id: Optional[int] = None
        self._end_char = "*"
        
    @staticmethod
    def config() -> ConfigPathOrDict:
        return Path(__file__).parent.parent / "schemas" / "kbc_quiz.json"

    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        return MAIN_MENU

    def teardown(self, request: JaxlIVRRequest) -> None:
        print("End of call")

    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        assert request["option"]
        if request.get("data", None) is not None:
            data = request["data"]
            assert data is not None
            assert data[-1] == self._end_char and self._current_question_id is not None
            # Repeat menu scenario
            if len(data) == 2 and data[0] == "0":
                self._current_operation = None
                return MAIN_MENU
            user_answer = data[0]
            response_prompt = check_answer(self._current_question_id, user_answer)
            return JaxlIVRResponse(
                prompt=response_prompt,
                num_characters=self._end_char,
                stream=None,
            )
        self._current_question_id = int(request["option"])
        return JaxlIVRResponse(
            prompt=get_question_prompt(self._current_question_id),
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