import dataclasses
import enum
import datetime
from typing import Optional


@dataclasses.dataclass(frozen=True)
class Duration:

    class Unit(enum.Enum):
        SECOND = enum.auto()
        DAY = enum.auto()
        WEEK = enum.auto()
        MONTH = enum.auto()
        YEAR = enum.auto()

    value: int
    unit: Unit

    _UNIT_STR = {
        Unit.SECOND: 'S',
        Unit.DAY: 'D',
        Unit.WEEK: 'W',
        Unit.MONTH: 'M',
        Unit.YEAR: 'Y',
    }

    def as_string(self) -> str:
        return '{} {}'.format(self.value, self._UNIT_STR[self.unit])


# Bar size of historical data. Use one of the constants below.
@dataclasses.dataclass(frozen=True)
class BarSize:

    class Unit(enum.Enum):
        SECOND = enum.auto()
        MINUTE = enum.auto()
        HOUR = enum.auto()
        DAY = enum.auto()
        WEEK = enum.auto()
        MONTH = enum.auto()

    value: int
    unit: Unit

    @classmethod
    def is_valid(cls, bar_size):
        return bar_size in _VALID_BAR_SIZES

    _UNIT_STR = {
        Unit.SECOND: 'sec',
        Unit.MINUTE: 'min',
        Unit.HOUR: 'hour',
        Unit.DAY: 'day',
        Unit.WEEK: 'week',
        Unit.MONTH: 'month',
    }

    def as_string(self) -> str:
        add_s = self.value > 1 or self.unit == BarSize.Unit.SECOND
        return '{} {}{}'.format(self.value, self._UNIT_STR[self.unit],
                                's' if add_s else '')


# Valid bar sizes: https://interactivebrokers.github.io/tws-api/historical_bars.html#hd_barsize
BAR_SIZE_1_SECS = BarSize(1, BarSize.Unit.SECOND)
BAR_SIZE_5_SECS = BarSize(5, BarSize.Unit.SECOND)
BAR_SIZE_10_SECS = BarSize(10, BarSize.Unit.SECOND)
BAR_SIZE_15_SECS = BarSize(15, BarSize.Unit.SECOND)
BAR_SIZE_30_SECS = BarSize(30, BarSize.Unit.SECOND)
BAR_SIZE_1_MIN = BarSize(1, BarSize.Unit.MINUTE)
BAR_SIZE_2_MIN = BarSize(2, BarSize.Unit.MINUTE)
BAR_SIZE_3_MIN = BarSize(3, BarSize.Unit.MINUTE)
BAR_SIZE_5_MIN = BarSize(5, BarSize.Unit.MINUTE)
BAR_SIZE_10_MIN = BarSize(10, BarSize.Unit.MINUTE)
BAR_SIZE_15_MIN = BarSize(15, BarSize.Unit.MINUTE)
BAR_SIZE_20_MIN = BarSize(20, BarSize.Unit.MINUTE)
BAR_SIZE_30_MIN = BarSize(30, BarSize.Unit.MINUTE)
BAR_SIZE_1_HOUR = BarSize(1, BarSize.Unit.HOUR)
BAR_SIZE_2_HOUR = BarSize(2, BarSize.Unit.HOUR)
BAR_SIZE_3_HOUR = BarSize(3, BarSize.Unit.HOUR)
BAR_SIZE_4_HOUR = BarSize(4, BarSize.Unit.HOUR)
BAR_SIZE_8_HOUR = BarSize(8, BarSize.Unit.HOUR)
BAR_SIZE_1_DAY = BarSize(1, BarSize.Unit.DAY)
BAR_SIZE_1_WEEK = BarSize(1, BarSize.Unit.WEEK)
BAR_SIZE_1_MONTH = BarSize(1, BarSize.Unit.MONTH)

_VALID_BAR_SIZES = set([
    BAR_SIZE_1_SECS,
    BAR_SIZE_5_SECS,
    BAR_SIZE_10_SECS,
    BAR_SIZE_15_SECS,
    BAR_SIZE_30_SECS,
    BAR_SIZE_1_MIN,
    BAR_SIZE_2_MIN,
    BAR_SIZE_3_MIN,
    BAR_SIZE_5_MIN,
    BAR_SIZE_10_MIN,
    BAR_SIZE_15_MIN,
    BAR_SIZE_20_MIN,
    BAR_SIZE_30_MIN,
    BAR_SIZE_1_HOUR,
    BAR_SIZE_2_HOUR,
    BAR_SIZE_3_HOUR,
    BAR_SIZE_4_HOUR,
    BAR_SIZE_8_HOUR,
    BAR_SIZE_1_DAY,
    BAR_SIZE_1_WEEK,
    BAR_SIZE_1_MONTH,
])


@dataclasses.dataclass
class HistoricalDataOptions(object):

    # https://interactivebrokers.github.io/tws-api/historical_bars.html#hd_what_to_show
    class Type(enum.Enum):
        TRADES = enum.auto()
        MIDPOINT = enum.auto()
        BID = enum.auto()
        ASK = enum.auto()
        BID_ASK = enum.auto()
        ADJUSTED_LAST = enum.auto()
        HISTORICAL_VOLATILITY = enum.auto()
        OPTION_IMPLIED_VOLATILITY = enum.auto()
        REBATE_RATE = enum.auto()
        FEE_RATE = enum.auto()
        YIELD_BID = enum.auto()
        YIELD_ASK = enum.auto()
        YIELD_BID_ASK = enum.auto()
        YIELD_LAST = enum.auto()

    class FormatTimeOption(enum.Enum):
        STRING = 1
        UNIX_SECONDS = 2

    end_datetime: Optional[datetime.datetime]
    duration: Duration
    bar_size: BarSize
    type: Type
    use_rth: bool = True
    stream: bool = False
    format_time: FormatTimeOption = FormatTimeOption.UNIX_SECONDS

    @classmethod
    def validate(cls, options):
        if not BarSize.is_valid(options.bar_size):
            raise ValueError('Invalid bar size: {}'.format(options.bar_size))
