import numpy as np

def trade_random_amount(agent, stock, exchange, sell):
    '''
    agent: the instance
    stock: the stock to trade
    timestamp: the timestamp to execute order
    sell: Boolean, True if sell, else buy

    Simple function that trades a random amount of stocks for an agent.
    Primarily intended for NoiseAgent.
    '''

    # extract necessary stucc
    portfolio = agent.portfolio
    orderbook = exchange.orderbooks[stock]

    timestamp = exchange.get_timestamp()

    highest_bid, lowest_ask = orderbook.highest_bid, orderbook.lowest_ask

    if sell:
        max_qty = portfolio.assets[stock]
        if max_qty == 0: return

        qty = np.random.randint(1, max_qty + 1)
        price = lowest_ask / np.random.normal(1.01, 0.01)
        order = agent.create_order(stock, price, qty, timestamp, buy=False)
        agent.submit_order(exchange, order)
    else:
        price = highest_bid * np.random.normal(1.01, 0.01)
        max_qty = agent.get_available_funds() // price
        if max_qty == 0: return
        qty = np.random.randint(1, max_qty + 1)
        order = agent.create_order(stock, price, qty, timestamp, buy=True)
        agent.submit_order(exchange, order)

    return


def get_historical_pe(stock, orderbook, periods, decay=1):
    n_shares = stock.company.n_shares

    P = min(stock.company.earnings.size, periods)
    earnings = stock.company.earnings.iloc[-P:][::-1]

    highest_bid = orderbook.highest_bid

    pe = 0
    for i, (day, earning) in enumerate(earnings.iteritems()):
        eps = earning / n_shares
        if i == 0:
            pe += highest_bid / eps
        else:
            pe += (stock.prices[day] / eps) * (decay ** i)

    return pe / P


def trading_momentum(stock, orderbook, periods, include_intraday=True):
    P = min(len(stock.prices), periods)

    prev = stock.prices[-P]
    now = orderbook.lowest_ask if include_intraday else stock.prices[-1]

    return np.log(now) - np.log(prev)
