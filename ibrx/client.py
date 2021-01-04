import threading
import time
import uuid

from ibapi import client, wrapper
from rx.subject import ReplaySubject

from xlab.trading.ibapi.mess import message_client, message_wrapper


class IbApiClient(object):

    def __init__(self, ip_addr: str, port: int, client_id: int):
        self._subject = ReplaySubject()
        self._message_wrapper = message_wrapper.IbApiMessageWrapper(self._subject)
        self._eclient = client.EClient(self._message_wrapper)
        self.message_client = message_client.IbApiMessageClient(
            self._eclient, lambda: uuid.uuid4().int & (1 << 16) - 1,
            self._subject)

        self._eclient.connect(ip_addr, port, client_id)

        self._thread = threading.Thread(target=self._eclient.run)
        self._thread.start()
