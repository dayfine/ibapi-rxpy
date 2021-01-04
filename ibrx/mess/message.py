import dataclasses
import enum
from typing import Any


class IbApiMessageType(enum.Enum):
    ERROR = enum.auto()
    ACCOUNT_SUMMARY = enum.auto()
    ACCOUNT_SUMMARY_END = enum.auto()
    POSITION = enum.auto()
    POSITION_END = enum.auto()


@dataclasses.dataclass
class IbApiMessage(object):
    type: IbApiMessageType
    payload: Any
