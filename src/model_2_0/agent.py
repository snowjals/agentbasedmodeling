from portfolio import Portfolio
from order import Order
import numpy as np


class Agent:
    def __init__(self, id, assets, initial_cash):
        '''
        id: int, the identifier of the agent.
        assets: List of stocks and bonds to be traded.
        initial_cash: float, the number of cash the agent starts with.

        Generates an Agent instance with an empty portfolio; It only consists
        of `initial_cash` (all stocks have quantity 0.0).
        '''
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



class NoiseAgent(Agent):
    def __init__(self, id, assets, initial_cash, trading_prob):
        super().__init__(id, assets, initial_cash)
        self.trading_prob = trading_prob

    def update_portfolio(self, exchange):
        portfolio = self.portfolio
        timestamp = exchange.get_timestamp()

        for each in portfolio.get_stocks():
            should_I_trade = np.random.choice([True, False], p=(self.trading_prob, 1-self.trading_prob))
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
