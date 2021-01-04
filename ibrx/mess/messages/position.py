import dataclasses
from typing import List, NewType, Optional, Set, Union

from ibapi import contract
from rx.core.typing import Observable
from rx import operators as _

from ibrx.mess.message import IbApiMessageType, IbApiMessage

@dataclasses.dataclass
class Position(object):
    account: str
    contract: contract.Contract
    size: float
    average_cost: float


def collect(messages: Observable[IbApiMessage]) -> Observable[List[Position]]:
    return messages.pipe(
        _.filter(lambda m: _is_position(m) or _is_position_end(m)),
        _.take_while(lambda m: not _is_position_end(m)),
        _.map(_unpack_position),
        _.reduce(lambda positions, position: positions.extend(position),
                 []),
    )


def _is_position(m: IbApiMessage) -> bool:
    return m.type == IbApiMessageType.POSITION


def _is_position_end(m: IbApiMessage) -> bool:
    return m.type == IbApiMessageType.POSITION_END

def _unpack_position(m: IbApiMessage) -> Position:
    return Position(*m.payload)
