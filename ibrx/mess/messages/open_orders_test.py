import unittest

from hamcrest import anything, all_of, assert_that, contains_exactly, empty, equal_to, has_property
from hamcrest.core.base_matcher import BaseMatcher
from ibapi import contract as ib_contract
from ibapi import order as ib_order
from ibapi import order_state as ib_order_state
from rx import create, empty as empty_obs, from_iterable

from ibrx.mess.message import IbApiMessageType, IbApiMessage
from ibrx.mess.messages import open_orders


def _contract1():
    contract = ib_contract.Contract()
    contract.conId = 265598
    contract.symbol = 'AAPL'
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.localSymbol = 'AAPL'
    contract.tradingClass = 'NMS'
    return contract


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


def _contract2():
    contract = ib_contract.Contract()
    contract.conId = 43645865
    contract.symbol = 'IBKR'
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    contract.localSymbol = 'IBKR'
    contract.tradingClass = 'NMS'
    return contract


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

    def _assert_eq_open_orders(self, actual, expected):
        assert_that(actual.order_id, equal_to(expected.order_id))
        assert_that(actual.contract, equal_to(expected.contract))
        assert_that(actual.order, equal_to(expected.order))
        assert_that(actual.order_state, equal_to(expected.order_id))

    def test_empty_observable(self):
        obs = open_orders.collect(empty_obs())

        assert_that(obs.run(), empty())

    def test_collect_works(self):
        obs = open_orders.collect(
            from_iterable([
                IbApiMessage(type=IbApiMessageType.OPEN_ORDER,
                             payload=(0, _contract1(), _order1(),
                                      _order_state1())),
                IbApiMessage(type=IbApiMessageType.OPEN_ORDER,
                             payload=(15, _contract2(), _order2(),
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
