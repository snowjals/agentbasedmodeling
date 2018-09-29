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

        print(f'submitting {order}')
        self.orderbooks[order.asset].submit(order, try_to_match=True)

    def end_of_day(self):
        for stock in self.orderbooks.keys():
            orderbook = self.orderbooks[stock]
            last_close = orderbook.get_last_completed()
            if last_close == 0:  # no trade is done
                last_close = stock.get_last_price()

            stock.add_price(last_close)
            orderbook.cancel_all_pending_orders()
