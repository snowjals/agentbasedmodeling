import numpy as np


def trade_random_amount(agent, stock, exchange, sell, max_qty=None):
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
        if max_qty is not None:
            max_qty = min(max_qty, portfolio.assets[stock])
        else:
            max_qty = portfolio.assets[stock]  # `max_qty` cannot be greater than what we have
            # max_qty = max_qty or portfolio.assets[stock]
        if max_qty == 0: return

        qty = np.random.randint(1, max_qty + 1)
        price = lowest_ask / np.random.normal(1.01, 0.01)
        order = agent.create_order(stock, price, qty, timestamp, buy=False)
        agent.submit_order(exchange, order)
    else:
        price = highest_bid * np.random.normal(1.01, 0.01)
        if max_qty is not None:
            max_qty = min(agent.get_available_funds() // price, max_qty)
        else:
            max_qty = agent.get_available_funds() // price  # `max_qty` cannot be greater than what we can afford with cash

        if max_qty == 0: return
        qty = np.random.randint(1, max_qty + 1)
        order = agent.create_order(stock, price, qty, timestamp, buy=True)
        agent.submit_order(exchange, order)

    return


def trade_target_portfolio(agent, exchange):
    '''
    agent: instance of agent
    exchange: instance of agent

    Will try to place orders so that the `agent.target_portfolio` is eventually
    achieved
    '''

    # do a random perutation on the target portfolio
    perm = np.random.permutation(list(agent.target_portfolio.items()))
    for stock, target_weight in perm:
        # since each iteration can place order, we need to calculate on each step
        # the total value of our agent.
        cash_available = agent.get_available_funds()  # noqa
        total_value = agent.get_total_funds()

        try:
            current_qty = agent.portfolio.assets[stock]
        except KeyError:
            current_qty = 0

        current_weight = (current_qty * stock.get_last_price()) / total_value

        if np.abs(target_weight - current_weight) < 0.02:
            continue  # too small.
        else:
            pass
            # print(f'{target_weight:.2f}, {current_weight:.2f}')

        if target_weight > current_weight:
            buy_qty = (target_weight - current_weight) * total_value // stock.get_last_price()
            agent.buy_stock(stock, exchange, buy_qty)
        elif target_weight < current_weight:
            sell_qty = (current_weight - target_weight) * total_value // stock.get_last_price()
            agent.sell_stock(stock, exchange, sell_qty)


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



