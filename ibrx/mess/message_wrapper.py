from typing import Any

from ibapi import wrapper
from rx.core.typing import Subject

from ibrx.mess.message import IbApiMessageType, IbApiMessage


class IbApiMessageWrapper(wrapper.EWrapper):

    def __init__(self, subject: Subject):
        self._subject = subject

    def _publish_message(self, msg_type: IbApiMessageType, payload: Any):
        self._subject.on_next(IbApiMessage(type=msg_type, payload=payload))

    # Start of EWrapper methods to be overriden.
    def error(self, *args):
        super().error(*args)
        self._publish_message(IbApiMessageType.ERROR, args)

    def accountSummary(self, *args):
        super().accountSummary(*args)
        self._publish_message(IbApiMessageType.ACCOUNT_SUMMARY, args)

    def accountSummaryEnd(self, *args):
        super().accountSummaryEnd(*args)
        self._publish_message(IbApiMessageType.ACCOUNT_SUMMARY_END, args)
