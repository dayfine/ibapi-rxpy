import unittest

from hamcrest import anything, all_of, assert_that, contains_exactly, empty, equal_to, has_property
from rx import empty as empty_obs, from_iterable

from ibrx.mess.message import IbApiMessageType, IbApiMessage
from ibrx.mess.messages import position, test_utils


class PositionTest(unittest.TestCase):

    def test_empty_observable(self):
        obs = position.collect(empty_obs())

        assert_that(obs.run(), empty())

    def test_collect_works(self):
        obs = position.collect(
            from_iterable([
                IbApiMessage(type=IbApiMessageType.POSITION,
                             payload=('DU123', test_utils.appl_contract(),
                                      100.0, 123.45)),
                IbApiMessage(type=IbApiMessageType.POSITION,
                             payload=('DU123', test_utils.ibkr_contract(), 1.0,
                                      45.6789)),
            ]))

        # TODO: for now, Contract, etc cannot be tested naively as they do not have __eq__ defined.
        assert_that(
            obs.run(),
            contains_exactly(
                all_of(
                    has_property('account', equal_to('DU123')),
                    has_property('contract', anything()),
                    has_property('size', equal_to(100.0)),
                    has_property('average_cost', equal_to(123.45)),
                ),
                all_of(
                    has_property('account', equal_to('DU123')),
                    has_property('contract', anything()),
                    has_property('size', equal_to(1.0)),
                    has_property('average_cost', equal_to(45.6789)),
                )))


if __name__ == '__main__':
    unittest.main()
