import dataclasses
import enum
from typing import Any


class IbApiMessageType(enum.Enum):
    ACCOUNT_SUMMARY = enum.auto()
    ACCOUNT_SUMMARY_END = enum.auto()
    ERROR = enum.auto()
    HISTORICAL_DATA = enum.auto()
    HISTORICAL_DATA_END = enum.auto()
    NEXT_VALID_ID = enum.auto()
    OPEN_ORDER = enum.auto()
    OPEN_ORDER_END = enum.auto()
    POSITION = enum.auto()
    POSITION_END = enum.auto()


@dataclasses.dataclass
class IbApiMessage(object):
    type: IbApiMessageType
    payload: Any = None
