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
    def error(self, *args):
        super().error(*args)
        self._publish_message(IbApiMessageType.ERROR, args)

    @overrides
    def accountSummary(self, *args):
        super().accountSummary(*args)
        self._publish_message(IbApiMessageType.ACCOUNT_SUMMARY, args)

    @overrides
    def accountSummaryEnd(self, *args):
        super().accountSummaryEnd(*args)
        self._publish_message(IbApiMessageType.ACCOUNT_SUMMARY_END, args)

    @overrides
    def position(self, *args):
        super().position(*args)
        self._publish_message(IbApiMessageType.POSITION, args)

    @overrides
    def positionEnd(self, *args):
        super().positionEnd(*args)
        self._publish_message(IbApiMessageType.POSITION_END, args)
