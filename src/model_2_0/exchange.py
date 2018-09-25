from orderbook import Orderbook


class Exchange:

    def __init__(self, n_agents, market_portfolio):
        self.n_agents = n_agents
        self.portfolio = market_portfolio
        self.orderbooks = {}
        self.reset_orderbooks()
        self.timestamp = None

    def get_timestamp(self):
        return self.timestamp

    def reset_orderbooks(self):
        for each in self.portfolio.get_stocks():
            bid, ask = each.get_last_price(), each.get_last_price()
            self.orderbooks[each] = Orderbook(bid, ask, [], [])

    def submit_order(self, order):
        if order.asset not in self.orderbooks.keys():
            raise ValueError('this is bad.')

        self.orderbooks[order.asset].submit(order, try_to_match=True)
