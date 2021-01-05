import dataclasses
from typing import Dict, List, NewType

from ibapi import contract
from ibapi import order
from ibapi import order_state

from rx import empty
from rx.core.typing import Observable
from rx import operators as _

from ibrx.mess.message import IbApiMessageType, IbApiMessage

OrderId = NewType('OrderId', int)


@dataclasses.dataclass
class OpenOrder(object):
    order_id: OrderId
    contract: contract.Contract
    order: order.Order
    order_state: order_state.OrderState


def collect(messages: Observable[IbApiMessage]) -> Observable[List[OpenOrder]]:
    # OpenOrders might emit (effective synchronously) something like:
    #  1, (end), 0, 1, (end)
    # Simply ending on the first 'end' would miss order 0, so wait up 1 sec.
    # Note how OPEN_ORDER_END is ignored as a result.
    return messages.pipe(
        _.timeout(0.1), _.on_error_resume_next(empty()),
        _.filter(lambda m: _is_open_order(m)),
        _.reduce(lambda orders, data: _add_data_to_orders(data, orders), {}),
        _.map(lambda orders_map: list(orders_map.values())))


def _is_open_order(m: IbApiMessage) -> bool:
    return m.type == IbApiMessageType.OPEN_ORDER


def _add_data_to_orders(
        data: IbApiMessage,
        orders: Dict[OrderId, OpenOrder]) -> Dict[OrderId, OpenOrder]:
    if _is_open_order(data):
        open_order = _unpack_open_order(data)
        orders[open_order.order_id] = open_order
    return orders


def _unpack_open_order(m: IbApiMessage):
    return OpenOrder(*m.payload)
