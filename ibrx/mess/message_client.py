from contextlib import ExitStack
from typing import Callable

from ibapi import client
from ibapi import account_summary_tags
from rx.core.typing import Observable
from rx import operators as ops

from ibrx.mess.message import IbApiMessageType
from ibrx.mess.messages.account_summary import *


class IbApiMessageClient:

    def __init__(self, eclient: client.EClient, id_gen: Callable[..., int],
                 messages: Observable):
        self._eclient = eclient
        self._id_gen = id_gen
        self._messages = messages

    def get_account_summary(self):
        request_id = self._id_gen()
        self._eclient.reqAccountSummary(
            request_id, "All", account_summary_tags.AccountSummaryTags.AllTags)

        with ExitStack() as stack:
            stack.callback(
                lambda: self._eclient.cancelAccountSummary(request_id))


            print('subscribing')
            acct_summary_messages.subscribe(lambda msg: print(msg))
            acct_summary_messages.run()
