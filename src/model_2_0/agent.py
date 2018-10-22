import numpy as np
import itertools

from portfolio import Portfolio
from order import Order
import utils
from stock import Stock
from utils import sigmoid
import trading_utils as tu


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
        self.traget_portfolio = None

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

    def find_target_portfolio(self, exchange):
        '''
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

    def get_total_funds(self):
        cash = self.get_available_funds()

        portfolio = self.portfolio
        market_value = 0
        for stock in portfolio.get_stocks():
            qty = portfolio.assets[stock]
            market_value += stock.get_last_price() * qty
        return market_value + cash

    def receive_dividends(self, stock, div_per_share):
        qty = self.portfolio.assets[stock]
        if qty <= 0:
            print('says receive dividends even though this shouldnt happen')
            import ipdb; ipdb.set_trace()
            return

        payout = div_per_share * qty
        self.portfolio.update_cash(payout)

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

            if self not in order.asset.company.shareholders:
                # print('adding to shareholders')
                order.asset.company.shareholders.append(self)

        else:  # sell
            cash_delta = order.executed_price * order.executed_quantity
            portfolio.update_cash(cash_delta)

            if portfolio.assets[order.asset] == 0:
                try:
                    order.asset.company.shareholders.remove(self)
                except ValueError:
                    pass

    def summary(self):
        portfolio = self.portfolio
        cash_avail = portfolio.get_cash_amount()
        market_value = self.get_total_funds() - cash_avail

        print('----------------')
        print(f'id:\t\t{self.id}')
        print(f'Cash:\t\t{cash_avail}')
        print(f'Market cap:\t{market_value}')
        print(f'Total:\t\t{market_value+cash_avail}')
        print()
        for stock in portfolio.get_stocks():
            qty = portfolio.assets[stock]
            price = stock.prices[-1]
            print(f'{stock.ticker}\tQty={qty}\tprice={price:.1f}\t(total {qty*price:.1f})')

    def __repr__(self):
        portfolio = self.portfolio
        cash_avail = portfolio.get_cash_amount()
        market_value = 0
        for stock in portfolio.get_stocks():
            qty = portfolio.assets[stock]
            market_value += stock.get_last_price() * qty

        return f'{self.id} w/ cash {cash_avail} and market value {market_value}'


class ValueAgent(Agent):
    def __init__(self, id, assets, initial_cash, epsilon, r_e, theta):
        super().__init__(id, assets, initial_cash)
        self.epsilon = epsilon
        self.r_e = r_e
        self.theta = theta

    def calculate_expected_asset_value(self, asset):
        # import ipdb;ipdb.set_trace()
        if type(asset) == Stock or True:
            '''
            (loosely) based on 'How learning in financial markets generates
            excess volatility and predictability in stock prices' by Allan G. Timmermann

            '''
            stock = asset
            return 25  # TODO: fix value investor..

            yields = stock.get_n_last_dividend_yields(self.theta)
            mu = np.mean(yields)
            sgm = np.var(yields)
            if np.isnan(sgm):
                sgm = 1
            # import ipdb;ipdb.set_trace()

            g = np.exp(mu + sgm / 2)
            D = stock.get_n_last_dividend_payouts(1)[0]
            value = g / (1 + self.r_e - g) * D
            return value

    def find_target_portfolio(self, exchange):
        '''
        populates `self.target_portfolio` of weights that the agent will
        try to reach.
        '''
        self.target_portfolio = {}

        for sector, g in itertools.groupby(exchange.portfolio.get_stocks(),
                                           lambda x: x.company.sector):
            g = np.array(list(g))  # make a array, so it can be reused

            pe_values = [tu.get_historical_pe(stock,
                                              orderbook=exchange.orderbooks[stock],
                                              periods=self.theta,
                                              decay=1) for stock in g]
            pe_values = np.array(pe_values)

            mean_pe = np.mean(pe_values)
            long_indices = np.argwhere(pe_values < mean_pe).flatten()

            weights = np.random.uniform(0, np.maximum(0, pe_values - mean_pe))
            # weights = np.random.uniform(size=long_indices.size)
            # print(pe_values)
            import utils
            utils.cprint(f'mean: {mean_pe:.2f} ' + ' '.join(['{}{:.2f}'.format('[g]' if e < mean_pe else '[r]', e) for e in pe_values]))

            short_stocks = np.array(g)[~long_indices]
            long_stocks = np.array(g)[long_indices]  # get those we will go long
            for stock, weight in zip(long_stocks, weights):
                self.target_portfolio[stock] = weight

            for stock in short_stocks:
                self.target_portfolio[stock] = 0.0
            # import ipdb; ipdb.set_trace()

        V = sum(self.target_portfolio.values())
        if V == 0: return  # in this special case, all are above mean.
        self.target_portfolio = {k: v / V for (k, v) in self.target_portfolio.items()}
        X = np.array(list(self.target_portfolio.values()))
        # print(X)
        # print(max(self.target_portfolio.values()))

    def update_portfolio(self, exchange):
        if exchange.get_timestamp().day % self.theta == 3:
            self.find_target_portfolio(exchange)
        else:
            try:
                tu.trade_target_portfolio(self, exchange)
            except AttributeError: pass

    def buy_stock(self, stock, exchange, qty=None):
        cash_avail = self.portfolio.get_cash_amount()
        price = exchange.orderbooks[stock].lowest_ask * np.random.normal(1.01, .01)
        max_qty = cash_avail // price

        if qty is not None and qty > max_qty:
            qty = max_qty  # impossible
        if max_qty <= 0: return

        qty = np.random.randint(1, max_qty + 1)
        order = self.create_order(stock, price, qty, exchange.get_timestamp(), buy=True)
        self.submit_order(exchange, order)

    def sell_stock(self, stock, exchange, qty=None):
        '''
        qty: the quantity to sell.

        Performs a check; will sell `min(stock_holdings, qty)` if `qty` is None. Otherwise
        sells asset_holdings of `stock_holdings`.
        '''
        max_qty = self.portfolio.assets[stock]
        if qty is not None and qty > max_qty:
            qty = max_qty
        else:
            qty = max_qty

        if qty == 0: return

        price = exchange.orderbooks[stock].highest_bid / np.random.normal(1.01, .01)
        order = self.create_order(stock, price, qty, exchange.get_timestamp(), buy=False)
        self.submit_order(exchange, order)


class NoiseAgent(Agent):
    def __init__(self, id, assets, initial_cash, trading_intensity):
        super().__init__(id, assets, initial_cash)
        self.trading_intensity = trading_intensity

    def update_portfolio(self, exchange):
        portfolio = self.portfolio
        timestamp = exchange.get_timestamp()

        # import ipdb; ipdb.set_trace()
        for each in portfolio.get_stocks():
            should_I_trade = utils.biased_bernoulli(self.trading_intensity / exchange.steps_per_day)
            if not should_I_trade: continue

            do_sell = np.random.choice([True, False])
            tu.trade_random_amount(self, each, exchange, sell=do_sell)


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
            orderbook = exchange.orderbooks[stock]
            highest_bid, lowest_ask = orderbook.get_bid_ask(stock)

            enough_history = len(stock.prices) > self.theta
            if not enough_history: continue

            div_period = min(stock.company.dividends.size, self.theta)
            # total dividend per share in period
            cumulative_dividends = stock.company.dividends.iloc[-div_period:].sum() / stock.company.n_shares
            D = cumulative_dividends

            momentum = tu.trading_momentum(stock, orderbook, self.theta, include_intraday=True)
            momentum_up = momentum > self.epsilon
            momentum_down = momentum < -self.epsilon
            # momentum_up = np.log(highest_bid + D) - np.log(stock.prices[-self.theta]) > self.epsilon  # noqa
            # momentum_down = np.log(lowest_ask  + D) - np.log(stock.prices[-self.theta]) < -self.epsilon  # noqa
            # momentum_up = np.log(highest_bid) - np.log(stock.prices[-self.theta]) > self.epsilon
            # momentum_down = np.log(lowest_ask + sum(stock.dividends[-self.theta:])) ) - np.log(stock.prices[-self.theta]) < -self.epsilon
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
