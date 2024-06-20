"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

import math
import os
import random
from abc import abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type, TypedDict, Union
from urllib.parse import urlparse

from unittest import TestCase


# PKS is a following representation:
#
# {
#     "ivrs": {
#         1234: {
#             "name": "main-menu",
#             "options": {
#                 4324: "1",
#                 5422: "2",
#             }
#         }
#     }
# }
PKS = Dict[str, Dict[int, Any]]


class IVRPhone(TypedDict):
    """IVR group structure within schema"""

    name: str
    e164: str


class IVRDevice(TypedDict):
    """IVR group structure within schema"""

    name: str
    device_id: List[int]


class IVRGroup(TypedDict):
    """IVR group structure within schema"""

    name: str
    members: List[str]


class IVROptionNeedsInput(TypedDict):
    """IVR option needs input structure within schema"""

    prompt: str
    end_character: str


class NextReference(TypedDict):
    """A NEXT type which references external schema file"""

    url: str
    name: str


class IVROption(TypedDict):
    """IVR option structure within schema"""

    name: str
    webhook: bool
    needs_input: Optional[IVROptionNeedsInput]
    confirm_input: bool
    next: Optional[Union[str, NextReference]]
    groups: Optional[List[str]]
    devices: Optional[List[str]]
    phone: Optional[str]


class IVR(TypedDict):
    """IVR structure within schema"""

    name: str
    webhook: bool
    greeting_message: str
    options: Dict[str, IVROption]


class IVRConfig(TypedDict):
    """IVR config schema"""

    phones: List[IVRPhone]
    devices: List[IVRDevice]
    groups: List[IVRGroup]
    ivrs: List[IVR]


class JaxlIVRResponse(TypedDict):
    """Expected response by Jaxl IVR server from webhooks."""

    # To provide prompt audio, a publicly hosted wav file URL
    # can also be returned.  For this to work, prompt must contain
    # only a single string which must be a URL starting with http:// or https://
    #
    # If you are hosting the wav file within your project directory,
    # also override `BaseJaxlIVRWebhook.paths` method within your implementation.
    prompt: List[str]
    # When an integer, this value represents number of characters to expect from the user
    # When a string, this value represents the ending character i.e. the character after which
    # system will stop taking further user inputs and proceed with IVR flow.
    num_characters: Union[int, str]
    # Optionally, configure system to start polling the webhook implementation
    # so that IVR can stream responses to the user
    stream: Optional[float]


class JaxlIVREvent(Enum):
    """Possible IVR events."""

    SETUP = 1
    OPTION = 2
    TEARDOWN = 3
    STREAM = 4


class JaxlIVRState(TypedDict):
    """Fixed & adhoc data associated with IVR state"""

    call_id: int
    from_number: str
    to_number: str


def generate_random_state() -> JaxlIVRState:
    """Returns randomly generated call_id, from_number and to_number."""
    call_id = random.randint(int(math.pow(10, 2)), int(math.pow(10, 5)))
    from_number = f"+91{random.randint(9000000000, 9999999999)}"
    to_number = f"+91{random.randint(9000000000, 9999999999)}"
    return JaxlIVRState(call_id=call_id, from_number=from_number, to_number=to_number)


def state_to_qs(state: JaxlIVRState) -> str:
    """Converts state to query string."""
    state = generate_random_state()
    return (
        f"call_id={state['call_id']}"
        + f"&from_number={state['from_number']}&to_number={state['to_number']}"
    )


class JaxlIVRRequest(TypedDict):
    """IVR Webhook request payload."""

    # Corresponds to "name" in ivr.json
    # Mapped locally because server is agnostic
    # of name mentioned in ivr.json file
    name: str

    # Corresponds to JaxlIVREvent
    event: int
    pk: int

    # One of possible keypad characters
    # that end user can enter via phone dialers
    option: Optional[str]

    # Following values only available when
    # webhook is invoked for a real call
    #
    # For simulations, this data CAN be provided
    # using simulation query string in the url directly
    state: Optional[JaxlIVRState]
    # Last input received from the user.  This is only populated when
    # prior JaxlIVRResponse.num_characters > 1 or num_characters was a string
    # representing ending character.
    data: Optional[str]


ConfigPathOrDict = Union[Path, IVRConfig]

STARTING_IN = "Starting in"


class BaseJaxlIVRWebhook:
    """Jaxl IVR interface."""

    @staticmethod
    def paths() -> Optional[Dict[str, Path]]:
        """Webhook can provide optional mapping of
        url path (string) to file path (Path) for serving static data."""
        return None

    @staticmethod
    @abstractmethod
    def config() -> ConfigPathOrDict:
        """Return a Path to related config or directly a dict representing IVR schema json."""
        raise NotImplementedError()

    @abstractmethod
    def setup(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        """Invoked when an IVR configured as webhook=true is triggered."""
        raise NotImplementedError()

    @abstractmethod
    def teardown(self, request: JaxlIVRRequest) -> None:
        """Called for every IVR once user journey has ended."""

    @abstractmethod
    def handle_option(self, request: JaxlIVRRequest) -> JaxlIVRResponse:
        """Respond to options configured as webhook=true."""
        raise NotImplementedError()

    @abstractmethod
    def stream(
        self,
        request: JaxlIVRRequest,
        chunk_id: int,
        sstate: Any,
    ) -> Optional[Tuple[Any, JaxlIVRResponse]]:
        """Called when a prior JaxlIVRResponse was sent with stream=<interval>.

        NOTE: All responses from stream must also pass stream=<interval>.
        Passing stream=None will break the stream and proceed to next step in the IVR.

        NOTE: chunk_id is an integer which will start from 0 when stream start
        and is incremented by 1 when stream method is called within the same ongoing stream request.

        NOTE: Return type must be 2-tuple where 1st element is internal state of stream
        to persist between subsequent invocation of webhook.stream method and 2nd element
        is the response to return.
        """
        raise NotImplementedError()

    @staticmethod
    def not_implemented(stream: Optional[float] = None) -> JaxlIVRResponse:
        """Utility to return not implemented response for unhandled scenarios."""
        return JaxlIVRResponse(
            prompt=["Not implemented."],
            num_characters=0,
            stream=stream,
        )

    @staticmethod
    def invalid_input(
        num_characters: int = 1,
        stream: Optional[float] = None,
    ) -> JaxlIVRResponse:
        """Utility to return not implemented response for unhandled scenarios."""
        return JaxlIVRResponse(
            prompt=["Invalid input."],
            num_characters=num_characters,
            stream=stream,
        )

    @staticmethod
    def invalid_state(stream: Optional[float] = None) -> JaxlIVRResponse:
        """Utility to return not implemented response for unhandled scenarios."""
        return JaxlIVRResponse(
            prompt=["Invalid state."],
            num_characters=0,
            stream=stream,
        )

    @staticmethod
    def countdown(
        total: int,
        chunk_id: int,
        every: float = 1.0,
        stop_stream_on_0: bool = True,
        prelude: str = STARTING_IN,
    ) -> JaxlIVRResponse:
        """Utility method send streaming countdown responses."""
        starts_in = total - chunk_id
        # print("starts_in", starts_in)
        return JaxlIVRResponse(
            prompt=[prelude] if starts_in == total else [f"{starts_in}"],
            num_characters=1,
            stream=(
                every * 2
                if starts_in == total
                else (every if starts_in > 0 else (None if stop_stream_on_0 else every))
            ),
        )

    @staticmethod
    def url_for_path(path: str) -> str:
        """Returns URL for a path hosted by webhook."""
        assert path.startswith("/")
        parsed_url = urlparse(os.environ.get("JAXL_IVR_WEBHOOK_URL"))
        scheme = (
            parsed_url.scheme
            if isinstance(parsed_url.scheme, str)
            else parsed_url.scheme.decode()
        )
        netloc = (
            parsed_url.netloc
            if isinstance(parsed_url.netloc, str)
            else parsed_url.netloc.decode()
        )
        return f"{scheme}://{netloc}{path}"


class BaseJaxlIVRWebhookTestCase(TestCase):
    """Base test case for testing IVR webhooks"""

    webhook_klass: Type[BaseJaxlIVRWebhook]

    def setUp(self) -> None:
        if self.webhook_klass is None:
            raise ValueError("webhook_class must be set by the subclass")
        self.webhook = self.webhook_klass()
        self.state = generate_random_state()
        self.start_call_request: Optional[JaxlIVRRequest] = None
        self.start_call_response: Optional[JaxlIVRResponse] = None

    def webhook_name(self) -> str:
        """Returns webhook name (slug) under testing."""
        config = self.webhook.config()
        assert isinstance(config, Path)
        return config.name

    def start_call(self) -> None:
        """Start a new call to your IVR webhook."""
        self.start_call_request = JaxlIVRRequest(
            name="Reminders",
            event=JaxlIVREvent.SETUP.value,
            pk=self.state["call_id"],
            option=None,
            state=self.state,
            data=None,
        )
        self.start_call_response = self.webhook.setup(request=self.start_call_request)

    def choose_option(self, option: str) -> Tuple[JaxlIVRRequest, JaxlIVRResponse]:
        """Chooses provided option."""
        request = JaxlIVRRequest(
            name="Reminders",
            event=JaxlIVREvent.OPTION.value,
            pk=self.state["call_id"],
            option=option,
            state=self.state,
            data=None,
        )
        return request, self.webhook.handle_option(request=request)

    def choose_option_and_send(
        self, option: str, user_input: str
    ) -> Tuple[JaxlIVRRequest, JaxlIVRResponse]:
        """Choose an option and send user input."""
        self.choose_option(option)
        request = JaxlIVRRequest(
            name="Reminders",
            event=JaxlIVREvent.OPTION.value,
            pk=self.state["call_id"],
            option=option,
            state=self.state,
            data=user_input,
        )
        return request, self.webhook.handle_option(request=request)
