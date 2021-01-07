import unittest

from hamcrest import anything, all_of, assert_that, contains_exactly, empty, equal_to, has_property
from ibapi import order as ib_order
from ibapi import order_state as ib_order_state
from rx import create, empty as empty_obs, from_iterable

from ibrx.mess.message import IbApiMessageType, IbApiMessage
from ibrx.mess.messages import open_orders, test_utils


def _order1():
    order = ib_order.Order()
    order.orderId = 0
    order.clientId = 0
    order.permId = 1348231368
    order.orderType = 'MKT'
    order.action = 'BUY'
    order.totalQuantity = 100
    order.lmtPrice = 0.0
    order.tif = 'GTC'
    return order


def _order_state1():
    order_state = ib_order_state.OrderState()
    return order_state


def _order2():
    order = ib_order.Order()
    order.orderId = 15
    order.clientId = 123
    order.permId = 205780343
    order.orderType = 'MKT'
    order.action = 'BUY'
    order.totalQuantity = 1
    order.lmtPrice = 0.0
    order.tif = 'DAY'
    return order


def _order_state2():
    order_state = ib_order_state.OrderState()
    return order_state


class OpenOrderTest(unittest.TestCase):

    def test_empty_observable(self):
        obs = open_orders.collect(empty_obs())

        assert_that(obs.run(), empty())

    def test_collect_works(self):
        obs = open_orders.collect(
            from_iterable([
                IbApiMessage(type=IbApiMessageType.OPEN_ORDER,
                             payload=(0, test_utils.appl_contract(), _order1(),
                                      _order_state1())),
                IbApiMessage(type=IbApiMessageType.OPEN_ORDER,
                             payload=(15, test_utils.ibkr_contract(), _order2(),
                                      _order_state2())),
            ]))

        # TODO: for now, Contract, Order, OrderState, etc cannot be tested
        # naively as they do not have __eq__ defined.
        assert_that(
            obs.run(),
            contains_exactly(
                all_of(
                    has_property('order_id', equal_to(0)),
                    has_property('contract', anything()),
                    has_property('order', anything()),
                    has_property('order_state', anything()),
                ),
                all_of(
                    has_property('order_id', equal_to(15)),
                    has_property('contract', anything()),
                    has_property('order', anything()),
                    has_property('order_state', anything()),
                )))


if __name__ == '__main__':
    unittest.main()
