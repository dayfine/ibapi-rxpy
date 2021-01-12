import datetime
import unittest

from hamcrest import assert_that, calling, equal_to, is_, raises

from ibrx.types.historical_data import BarSize, Duration, HistoricalDataOptions, HistoricalDataType


class HistoricalDataTypeTest(unittest.TestCase):

    def test_duration_string_conversion(self):
        _Unit = Duration.Unit
        assert_that(Duration(15, _Unit.SECOND).as_string(), equal_to('15 S'))
        assert_that(Duration(99, _Unit.DAY).as_string(), equal_to('99 D'))
        assert_that(Duration(52, _Unit.WEEK).as_string(), equal_to('52 W'))
        assert_that(Duration(36, _Unit.MONTH).as_string(), equal_to('36 M'))
        assert_that(Duration(5, _Unit.YEAR).as_string(), equal_to('5 Y'))

    def test_bar_size_validation(self):
        _Unit = BarSize.Unit
        assert_that(BarSize.is_valid(BarSize(1, _Unit.HOUR)), is_(True))
        assert_that(BarSize.is_valid(BarSize(20, _Unit.MINUTE)), is_(True))
        assert_that(BarSize.is_valid(BarSize(20, _Unit.HOUR)), is_(False))

    def test_bar_size_string_conversion(self):
        _Unit = BarSize.Unit
        assert_that(BarSize(1, _Unit.SECOND).as_string(), equal_to('1 secs'))
        assert_that(BarSize(5, _Unit.SECOND).as_string(), equal_to('5 secs'))
        assert_that(BarSize(1, _Unit.MINUTE).as_string(), equal_to('1 min'))
        assert_that(BarSize(30, _Unit.MINUTE).as_string(), equal_to('30 mins'))
        assert_that(BarSize(1, _Unit.HOUR).as_string(), equal_to('1 hour'))
        assert_that(BarSize(5, _Unit.HOUR).as_string(), equal_to('5 hours'))
        assert_that(BarSize(1, _Unit.DAY).as_string(), equal_to('1 day'))
        assert_that(BarSize(1, _Unit.WEEK).as_string(), equal_to('1 week'))
        assert_that(BarSize(1, _Unit.MONTH).as_string(), equal_to('1 month'))

    def test_options_with_invalid_bar_size(self):
        options = HistoricalDataOptions(
            end_datetime=datetime.datetime(2020, 2, 29),
            duration=Duration(3, Duration.Unit.MONTH),
            bar_size=BarSize(20, BarSize.Unit.HOUR),
            type=HistoricalDataType.ADJUSTED_LAST)
        assert_that(
            calling(HistoricalDataOptions.validate).with_args(options),
            raises(ValueError))


if __name__ == '__main__':
    unittest.main()
