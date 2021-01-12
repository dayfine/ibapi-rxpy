from ibapi import contract

from ibrx import IbApiClient
from ibrx.types import historical_data

_IB_GATEWAY_PROD_PORT = 4001
_IB_GATEWAY_SIMULATED_PORT = 4002
_TWS_PROD_PORT = 7496
_TWS_SIMULATED_PORT = 7497


def main():
    ibapi_client = IbApiClient('', _IB_GATEWAY_PROD_PORT, 123)
    print('Account Summary: ', ibapi_client.get_account_summary())
    # positions = ibapi_client.get_positions()
    # print('\nPositions: ', positions)
    # print('\nOpen Orders: ', ibapi_client.get_open_orders())

    c = contract.Contract()
    c.symbol = 'AAPL'
    c.secType = 'STK'
    c.exchange = 'SMART'
    c.currency = 'USD'
    c.localSymbol = 'AAPL'

    hd = ibapi_client.get_historical_data(
        contract=c,
        data_options=historical_data.HistoricalDataOptions(
            end_datetime=None,
            duration=historical_data.Duration(
                2, historical_data.Duration.Unit.WEEK),
            bar_size=historical_data.BAR_SIZE_2_HOUR,
            type=historical_data.HistoricalDataOptions.Type.TRADES))

    print('\nHistorical data ', hd)


if __name__ == '__main__':
    main()
