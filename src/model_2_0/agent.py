from portfolio import Portfolio
from order import Order
import numpy as np
from utils import sigmoid


class Agent:
    def __init__(self, id, assets, initial_cash):
        '''
        id: int, the identifier of the agent.
        assets: List of stocks and bonds to be traded.
        initial_cash: float, the number of cash the agent starts with.

        Generates an Agent instance with an empty portfolio; It only consists
        of `initial_cash` (all stocks have quantity 0.0).
        '''
        self.id = id
        self.portfolio = Portfolio.empty_portfolio(assets)
        self.portfolio.set_cash_amount(initial_cash)
        self.pending_orders = []

    def submit_order(self, exchange, order):
        '''
        Submits a given order. Does book-keeping. Reduces `self.portfolio.cash`
        '''
        if not order.is_buy():  # sell
            self.portfolio.assets[order.asset] -= order.quantity
            exchange.submit_order(order)
            return

        elif self.sufficient_funds(order):
            cash_delta = -(order.bid * order.quantity)
            self.portfolio.update_cash(cash_delta)

            exchange.submit_order(order)

    def create_order(self, asset, price, quantity, timestamp, buy):
        '''
        Wrapper around Order.bid and Order.ask: Populates agent with `self`
        '''
        order_func = Order.bid if buy else Order.ask
        return order_func(agent=self,
                          asset=asset,
                          price=price,
                          quantity=quantity,
                          timestamp=timestamp,
                          order_type='limit')

    def update_portfolio(self, exchange):
        '''
        exchange: an instance of Exchange.

        To be implemented in the respective sub-class

        Method used to submit orders for an agent. Should potentially
        call `self.submit_order` with different orders.
        submit_order

        returns None
        '''
        pass

    def sufficient_funds(self, order):
        if not order.is_buy(): return True  # we always have enough cash to sell :)

        return order.bid * order.quantity <= self.get_available_funds()

    def get_available_funds(self):
        '''
        Returns the available funds for the agent.
        '''
        portfolio = self.portfolio
        cash_available = portfolio.get_cash_amount()
        return cash_available

    def update_asset_holdings(self, order):
        '''
        callback..
        order: Instance of an _executed_ order.
        '''
        portfolio = self.portfolio
        if order.is_buy():
            cash_delta = (order.bid - order.executed_price) * order.executed_quantity
            portfolio.update_cash(cash_delta)
            portfolio.assets[order.asset] += order.executed_quantity

        else:
            cash_delta = order.executed_price * order.executed_quantity
            portfolio.update_cash(cash_delta)

    def __repr__(self):
        portfolio = self.portfolio
        cash_avail = portfolio.get_cash_amount()
        market_value = 0
        for stock in portfolio.get_stocks():
            qty = portfolio.assets[stock]
            market_value += stock.get_last_price() * qty

        return f'{self.id} w/ cash {cash_avail} and market value {market_value}'


class NoiseAgent(Agent):
    def __init__(self, id, assets, initial_cash, trading_intensity):
        super().__init__(id, assets, initial_cash)
        self.trading_intensity = trading_intensity

    def update_portfolio(self, exchange):
        portfolio = self.portfolio
        timestamp = exchange.get_timestamp()

        for each in portfolio.get_stocks():
            should_I_trade = np.random.choice([True, False], p=(self.trading_intensity, 1-self.trading_intensity))
            if not should_I_trade: continue

            orderbook = exchange.orderbooks[each]
            highest_bid, lowest_ask = orderbook.highest_bid, orderbook.lowest_ask

            do_buy = np.random.choice([True, False])

            if do_buy:
                # AaaAAAaAAAaAaAaaaAAAa!!!
                price = highest_bid * np.random.normal(1.01, 0.01)
                if price == 0:
                    price = 24
                max_qty = self.get_available_funds() // price
                if max_qty == 0:
                    continue  # nvm, no noise
                qty = np.random.randint(1, max_qty + 1)
                order = self.create_order(each, price, qty, timestamp, buy=True)
                self.submit_order(exchange, order)

            else:
                max_qty = portfolio.assets[each]
                if max_qty == 0:
                    continue
                qty = np.random.randint(1, max_qty + 1)
                price = lowest_ask / np.random.normal(1.01, 0.01)
                order = self.create_order(each, price, qty, timestamp, buy=False)
                self.submit_order(exchange, order)


class TrendAgent(Agent):
    def __init__(self, id, assets, initial_cash, c, theta, epsilon):
        super().__init__(id, assets, initial_cash)
        self.id = id
        self.assets = assets
        self.c = c
        self.theta = theta
        self.epsilon = epsilon

    def update_portfolio(self, exchange):
        portfolio = self.portfolio
        timestamp = exchange.get_timestamp()

        for stock in portfolio.get_stocks():

            # don't do trade there is not enough price history.
            highest_bid, lowest_ask = exchange.orderbooks[stock].get_bid_ask(stock)

            enough_history = len(stock.prices) > self.theta
            if not enough_history: continue

            momentum_up = np.log(highest_bid) - np.log(stock.prices[-self.theta]) > self.epsilon
            momentum_down = np.log(lowest_ask) - np.log(stock.prices[-self.theta]) < -self.epsilon
            can_buy_one = portfolio.get_cash_amount() > lowest_ask
            can_sell_one = portfolio.assets[stock] > 0

            should_I_trade = (momentum_up and can_buy_one) or (momentum_down and can_sell_one)
            if not should_I_trade: continue

            if momentum_up and can_buy_one:  # it's going uuup
                max_qty = (sigmoid(self.c) * portfolio.get_cash_amount()) // lowest_ask
                if max_qty == 0: continue  # couldnt' afford after all with risk-aversion

                price = highest_bid * np.random.normal(1.01, 0.01)
                qty = np.random.randint(1, max_qty + 1)
                order = self.create_order(stock, price, qty, timestamp, buy=True)
                self.submit_order(exchange, order)

            if momentum_down and can_sell_one:
                max_qty = portfolio.assets[stock]
                if max_qty == 0:
                    continue
                qty = np.random.randint(1, max_qty + 1)
                price = highest_bid / np.random.normal(1.01, 0.01)
                order = self.create_order(stock, price, qty, timestamp, buy=False)
                self.submit_order(exchange, order)
