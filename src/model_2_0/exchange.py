from orderbook import Orderbook


class Exchange:

    def __init__(self, agents, market_portfolio):
        self.agents = agents
        self.n_agents = len(self.agents)
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

    def start_of_day(self):
        for stock, orderbook in self.orderbooks.items():
            stock.calculate_dividend()
            if stock.dividends[-1] > stock.prices[-1]:
                import ipdb;ipdb.set_trace()
            if stock.dividends[-1] > 0:
                orderbook.highest_bid -= stock.dividends[-1]
                orderbook.lowest_ask -= stock.dividends[-1]
                for agent in self.agents:
                    agent.receive_dividend(stock)  # possibly zero, if dont hold

    def end_of_day(self):
        for stock in self.orderbooks.keys():
            orderbook = self.orderbooks[stock]
            last_close = orderbook.get_last_completed()
            if last_close == 0:  # no trade is done
                last_close = stock.get_last_price()

            stock.add_price(last_close)
            orderbook.cancel_all_pending_orders()
