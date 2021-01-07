from ibapi import contract


def appl_contract():
    c = contract.Contract()
    c.conId = 265598
    c.symbol = 'AAPL'
    c.secType = 'STK'
    c.exchange = 'SMART'
    c.currency = 'USD'
    c.localSymbol = 'AAPL'
    c.tradingClass = 'NMS'
    return c


def ibkr_contract():
    c = contract.Contract()
    c.conId = 43645865
    c.symbol = 'IBKR'
    c.secType = 'STK'
    c.exchange = 'SMART'
    c.currency = 'USD'
    c.localSymbol = 'IBKR'
    c.tradingClass = 'NMS'
    return c
