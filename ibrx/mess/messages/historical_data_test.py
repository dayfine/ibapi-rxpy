import datetime
import unittest

from hamcrest import assert_that, equal_to, contains_exactly, empty
from ibapi.common import BarData as IbBarData
from rx import empty as empty_obs, from_iterable

from ibrx.mess.message import IbApiMessageType, IbApiMessage
from ibrx.mess.messages import historical_data
from ibrx.types import historical_data as types


class HistoricalDataTest(unittest.TestCase):

    def test_empty_observable(self):
        obs = historical_data.collect(empty_obs(), 0,
                                      types.HistoricalDataType.TRADES)

        assert_that(obs.run(), empty())

    def test_collect_historical_data(self):
        bar_data_1 = IbBarData()
        bar_data_1.date = '1515000000'
        bar_data_1.open = 1
        bar_data_1.high = 2
        bar_data_1.low = 1.5
        bar_data_1.close = 1.75
        bar_data_1.average = -1
        bar_data_1.volume = -1
        bar_data_1.barCount = -1

        bar_data_2 = IbBarData()
        bar_data_2.date = '1516000000'
        bar_data_2.open = 2
        bar_data_2.high = 3
        bar_data_2.low = 1.25
        bar_data_2.close = 2.25
        bar_data_2.average = -1
        bar_data_2.volume = -1
        bar_data_2.barCount = -1

        messages = [
            IbApiMessage(type=IbApiMessageType.HISTORICAL_DATA,
                         payload=(0, bar_data_1)),
            IbApiMessage(type=IbApiMessageType.HISTORICAL_DATA,
                         payload=(0, bar_data_2)),
        ]

        assert_that(
            historical_data.collect(from_iterable(messages), 0,
                                    types.HistoricalDataType.MIDPOINT).run(),
            contains_exactly(
                equal_to(
                    types.BarData(type=types.HistoricalDataType.MIDPOINT,
                                  time=datetime.datetime(2018, 1, 3, 17, 20),
                                  open=1,
                                  high=2,
                                  low=1.5,
                                  close=1.75)),
                equal_to(
                    types.BarData(type=types.HistoricalDataType.MIDPOINT,
                                  time=datetime.datetime(2018, 1, 15, 7, 6, 40),
                                  open=2,
                                  high=3,
                                  low=1.25,
                                  close=2.25))))

    def test_collect_historical_trade_data(self):
        bar_data_1 = IbBarData()
        bar_data_1.date = '1577000000'
        bar_data_1.open = 1
        bar_data_1.high = 2
        bar_data_1.low = 1.5
        bar_data_1.close = 1.75
        bar_data_1.average = 1.567
        bar_data_1.volume = 9414151
        bar_data_1.barCount = 3435

        bar_data_2 = IbBarData()
        bar_data_2.date = '1577003600'
        bar_data_2.open = 2
        bar_data_2.high = 3
        bar_data_2.low = 1.25
        bar_data_2.close = 2.25
        bar_data_2.average = 2.123
        bar_data_2.volume = 4543625
        bar_data_2.barCount = 3821
        messages = [
            IbApiMessage(type=IbApiMessageType.HISTORICAL_DATA,
                         payload=(0, bar_data_1)),
            IbApiMessage(type=IbApiMessageType.HISTORICAL_DATA,
                         payload=(0, bar_data_2)),
        ]

        assert_that(
            historical_data.collect(from_iterable(messages), 0,
                                    types.HistoricalDataType.TRADES).run(),
            contains_exactly(
                equal_to(
                    types.BarData(
                        type=types.HistoricalDataType.TRADES,
                        time=datetime.datetime(2019, 12, 22, 7, 33, 20),
                        open=1,
                        high=2,
                        low=1.5,
                        close=1.75,
                        trade_data=types.BarData.TradeData(volume=9414151,
                                                           average_price=1.567,
                                                           bar_count=3435))),
                equal_to(
                    types.BarData(
                        type=types.HistoricalDataType.TRADES,
                        time=datetime.datetime(2019, 12, 22, 8, 33, 20),
                        open=2,
                        high=3,
                        low=1.25,
                        close=2.25,
                        trade_data=types.BarData.TradeData(volume=4543625,
                                                           average_price=2.123,
                                                           bar_count=3821)))))


if __name__ == '__main__':
    unittest.main()
