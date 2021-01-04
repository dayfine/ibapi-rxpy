from xlab.trading.ibapi import client

_IB_GATEWAY_PROD_PORT = 4001
_IB_GATEWAY_SIMULATED_PORT = 4002


def main(argv):
    del argv  # Unused.

    ibapi_client = client.IbApiClient('', _IB_GATEWAY_SIMULATED_PORT, 123)
    ibapi_client.message_client.get_account_summary()


if __name__ == '__main__':
    main()
