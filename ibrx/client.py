from contextlib import ExitStack
import threading
from typing import List

from ibapi import client
from ibapi import account_summary_tags
from ibapi import contract
from ibapi import order
from rx import operators as _
from rx.subject import ReplaySubject

from ibrx.mess import message_wrapper
from ibrx.mess.message import IbApiMessageType
from ibrx.mess.messages import account_summary
from ibrx.mess.messages import historical_data
from ibrx.mess.messages import open_orders
from ibrx.mess.messages import position
from ibrx.types.historical_data import HistoricalDataOptions


class IbApiClient(object):

    def __init__(self, ip_addr: str, port: int, client_id: int):
        self._messages = ReplaySubject()
        self._message_wrapper = message_wrapper.IbApiMessageWrapper(
            self._messages)
        self._eclient = client.EClient(self._message_wrapper)

        self._eclient.connect(ip_addr, port, client_id)
        self._thread = threading.Thread(target=self._eclient.run)
        self._thread.start()

    def _next_valid_id(self) -> int:
        self._eclient.reqIds(-1)  # Argument is ignored
        return self._messages.pipe(
            _.first(lambda m: m.type == IbApiMessageType.NEXT_VALID_ID),
            _.map(lambda m: m.payload[0])).run()

    def get_account_summary(self) -> account_summary.AccountSummary:
        request_id = self._next_valid_id()
        self._eclient.reqAccountSummary(
            request_id, "All", account_summary_tags.AccountSummaryTags.AllTags)

        with ExitStack() as stack:
            stack.callback(
                lambda: self._eclient.cancelAccountSummary(request_id))
            obs = account_summary.collect(self._messages, request_id)
            return obs.run()

    def get_open_orders(self) -> List[open_orders.OpenOrder]:
        # reqAllOpenOrders is used instead of reqOpenOrders to include manual
        # orders. Also, reqAllOpenOrders does not initiate a subscription.
        self._eclient.reqAllOpenOrders()
        obs = open_orders.collect(self._messages)
        return obs.run()

    def get_positions(self) -> List[position.Position]:
        self._eclient.reqPositions()
        with ExitStack() as stack:
            stack.callback(self._eclient.cancelPositions)
            obs = position.collect(self._messages)
            return obs.run()

    def place_order(self, contract: contract.Contract, order: order.Order):
        self._eclient.placeOrder(self._next_valid_id(), contract, order)

    def cancel_order(self, order_id: int):
        self._eclient.cancelOrder(order_id)

    def get_historical_data(self, contract: contract.Contract,
                            data_options: HistoricalDataOptions):
        HistoricalDataOptions.validate(data_options)
        if data_options.stream:
            raise ValueError(
                'get_historical_data should not be called with |options.stream| = True'
            )

        request_id = self._next_valid_id()
        end_datetime_str = data_options.end_datetime.strftime(
            '%Y%m%d %H:%M%S') if data_options.end_datetime else ''
        self._eclient.reqHistoricalData(
            request_id,
            contract,
            endDateTime=end_datetime_str,
            durationStr=data_options.duration.as_string(),
            barSizeSetting=data_options.bar_size.as_string(),
            whatToShow=data_options.type.name,
            useRTH=data_options.use_rth,
            formatDate=data_options.format_time.value,
            keepUpToDate=False,
            chartOptions=None)
        obs = historical_data.collect(self._messages)
        return obs.run()
