from contextlib import ExitStack
from typing import Callable

from ibapi import client
from ibapi import account_summary_tags
from rx.core.typing import Observable
from rx import operators as ops

from ibrx.mess.message import IbApiMessageType
from ibrx.mess.messages import account_summary


class IbApiMessageClient:

    def __init__(self, eclient: client.EClient, id_gen: Callable[..., int],
                 messages: Observable):
        self._eclient = eclient
        self._id_gen = id_gen
        self._messages = messages

    def get_account_summary(self) -> account_summary.AccountSummary:
        request_id = self._id_gen()
        self._eclient.reqAccountSummary(
            request_id, "All", account_summary_tags.AccountSummaryTags.AllTags)

        with ExitStack() as stack:
            stack.callback(
                lambda: self._eclient.cancelAccountSummary(request_id))
            obs = account_summary.collect(self._messages, request_id)
            return obs.run()
