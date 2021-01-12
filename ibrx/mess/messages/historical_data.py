import dataclasses
import datetime
from typing import List, Optional

from ibapi.common import BarData as IbBarData
from rx.core.typing import Observable
from rx import operators as _

from ibrx.mess.message import IbApiMessageType, IbApiMessage
from ibrx.types import historical_data as types


def collect(
        messages: Observable[IbApiMessage], request_id: int,
        data_type: types.HistoricalDataType) -> Observable[List[types.BarData]]:
    return messages.pipe(
        _.filter(
            lambda m: _is_historical_data(m) or _is_historical_data_end(m)),
        _.filter(lambda m: _request_id(m) == request_id),
        _.take_while(lambda m: not _is_historical_data_end(m)),
        _.map(lambda m: _unpack_historical_data(m, data_type)),
        _.reduce(lambda bars, bar: [*bars, bar], []),
    )


def _is_historical_data(m: IbApiMessage) -> bool:
    return m.type == IbApiMessageType.HISTORICAL_DATA


def _is_historical_data_end(m: IbApiMessage) -> bool:
    return m.type == IbApiMessageType.HISTORICAL_DATA_END


def _request_id(m: IbApiMessage) -> int:
    return m.payload[0]


def _unpack_historical_data(
        m: IbApiMessage, data_type: types.HistoricalDataType) -> types.BarData:
    _, ib_bar = m.payload
    return types.BarData(type=data_type,
                         time=datetime.datetime.fromtimestamp(int(ib_bar.date)),
                         open=ib_bar.open,
                         high=ib_bar.high,
                         low=ib_bar.low,
                         close=ib_bar.close,
                         trade_data=_unpack_trade_data(ib_bar, data_type))


def _unpack_trade_data(
        ib_bar: IbBarData,
        data_type: types.HistoricalDataType) -> types.BarData.TradeData:
    if data_type != types.HistoricalDataType.TRADES:
        return None
    return types.BarData.TradeData(volume=ib_bar.volume,
                                   average_price=ib_bar.average,
                                   bar_count=ib_bar.barCount)
