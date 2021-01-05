from ibrx import client

_IB_GATEWAY_PROD_PORT = 4001
_IB_GATEWAY_SIMULATED_PORT = 4002
_TWS_PROD_PORT = 7496
_TWS_SIMULATED_PORT = 7497


def main():
    ibapi_client = client.IbApiClient('', _IB_GATEWAY_SIMULATED_PORT, 123)
    print('Account Summary: ', ibapi_client.get_account_summary())
    print('Positions: ', ibapi_client.get_positions())
    print('Open Orders: ', ibapi_client.get_open_orders())


if __name__ == '__main__':
    main()
