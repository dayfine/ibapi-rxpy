from typing import Any

from ibapi import wrapper
from overrides import overrides
from rx.core.typing import Subject

from ibrx.mess.message import IbApiMessageType, IbApiMessage


class IbApiMessageWrapper(wrapper.EWrapper):

    def __init__(self, subject: Subject):
        self._subject = subject

    def _publish_message(self, msg_type: IbApiMessageType, payload: Any):
        self._subject.on_next(IbApiMessage(type=msg_type, payload=payload))

    # Start of EWrapper methods to be overriden.
    @overrides
    def accountSummary(self, *args):
        super().accountSummary(*args)
        self._publish_message(IbApiMessageType.ACCOUNT_SUMMARY, args)

    @overrides
    def accountSummaryEnd(self, *args):
        super().accountSummaryEnd(*args)
        self._publish_message(IbApiMessageType.ACCOUNT_SUMMARY_END, args)

    @overrides
    def error(self, *args):
        super().error(*args)
        self._publish_message(IbApiMessageType.ERROR, args)

    @overrides
    def historicalData(self, *args):
        super().historicalData(*args)
        self._publish_message(IbApiMessageType.HISTORICAL_DATA, args)

    @overrides
    def nextValidId(self, *args):
        super().nextValidId(*args)
        self._publish_message(IbApiMessageType.NEXT_VALID_ID, args)

    @overrides
    def openOrder(self, *args):
        super().openOrder(*args)
        self._publish_message(IbApiMessageType.OPEN_ORDER, args)

    @overrides
    def openOrderEnd(self, *args):
        super().openOrderEnd(*args)
        self._publish_message(IbApiMessageType.OPEN_ORDER_END, args)

    @overrides
    def position(self, *args):
        super().position(*args)
        self._publish_message(IbApiMessageType.POSITION, args)

    @overrides
    def positionEnd(self, *args):
        super().positionEnd(*args)
        self._publish_message(IbApiMessageType.POSITION_END, args)
