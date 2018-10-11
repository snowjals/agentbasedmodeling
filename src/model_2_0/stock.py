from asset import Asset
import numpy as np


class Stock(Asset):
    def __init__(self, ticker, price):
        '''
        ticker: string, the ticker symbol. Example: 'ticker'
        price: The initial price. It is stored in `self.prices`
        '''

        self.ticker = ticker
        self.prices = [price]
        self.div_period = 68
        self.dividends = [0]

    def get_last_price(self):
        return self.prices[-1]

    def add_price(self, new_price):
        self.prices.append(new_price)
        return

    def get_n_last_dividend_yields(self, n):
        # TODO: what if n > history.
        current_step = len(self.prices)
        steps_since_last_payout = current_step % self.div_period

        L = []
        for i in range(-steps_since_last_payout - 1, -self.div_period * n, -self.div_period):
            if abs(i) >= len(self.dividends): break
            if len(L) == n: break
            L.append(self.dividends[i] / self.prices[i])

        if len(L) == 0: return [0]
        return L

    def get_n_last_dividend_payouts(self, n):
        # TODO: what if n > history.
        current_step = len(self.prices)
        steps_since_last_payout = current_step % self.div_period

        L = []
        for i in range(-steps_since_last_payout - 1, -self.div_period * n, -self.div_period):
            if abs(i) >= len(self.dividends): break
            # if len(L) > 20: import ipdb; ipdb.set_trace()
            L.append(self.dividends[-i])

        if len(L) == 0: return [0]
        return L

    def _calculate_new_dividend_yield(self):
        '''
        Finds the new yield. Assumes that the current step pays out dividends.
        '''
        eta = 0.25
        M = 0.02
        dt = 1
        sigma = 0.2
        Y = 1.05
        lambda_ = 0.25
        k = lambda_ * Y

        prev_yield = self.dividends[-self.div_period] / self.prices[-self.div_period]

        dq = (Y-1) * np.random.choice([0, 1], p=[1-lambda_*dt, lambda_*dt])
        sgn = np.random.choice([-1, 1])
        dq = dq * sgn

        dz = np.random.normal(0, 1) * dt
        dx = prev_yield * eta * (M - prev_yield - k*lambda_) * dt + sigma * prev_yield * dz + dq
        y = max(0, prev_yield + dx)

        return y

    def calculate_dividend(self):
        current_step = len(self.prices)
        if current_step % self.div_period == 0:  # payout time
            dividend = self.prices[-1] * self._calculate_new_dividend_yield()
            self.dividends.append(dividend)
        else:
            self.dividends.append(0)  # no payout

    def __repr__(self):
        return f'[Stock {self.ticker}@{self.get_last_price()}]'
