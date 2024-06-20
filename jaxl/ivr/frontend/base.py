"""
Copyright (c) 2010-present by Jaxl Innovations Private Limited.

All rights reserved.

Redistribution and use in source and binary forms,
with or without modification, is strictly prohibited.
"""

from abc import abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, TypedDict, Union


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
