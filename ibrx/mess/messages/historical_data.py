from rx.core.typing import Observable
from rx import operators as _

from ibrx.mess.message import IbApiMessageType, IbApiMessage


def collect(messages: Observable[IbApiMessage]) -> Observable[str]:
    return messages.pipe(_.filter(lambda m: _is_historical_data(m)),
                         _.map(_unpack_historical_data))


def _is_historical_data(m: IbApiMessage) -> bool:
    return m.type == IbApiMessageType.HISTORICAL_DATA


def _unpack_historical_data(m: IbApiMessage):
    print(m)
