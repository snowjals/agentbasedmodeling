import pandas as pd
import numpy as np


class Company:
    def __init__(self, ticker, n_shares, cash, sector, yield_policy):
        '''
        n_shares: int, the number of shares
        cash: how much cash the company has
        sector: string, the sector it belongs to
        yield_policy: float, how much of earnings should be paid out
        '''

        self.ticker = ticker
        self.n_shares = n_shares
        self.sector = sector
        self.yield_policy = yield_policy

        self.earnings = pd.Series()
        self.earnings.name = 'day'
        self.cash = cash

        self.earnings.loc[0] = cash / 10  # set initial PE to 10

        self.dividends = pd.Series()
        self.dividends.name = 'day'

        self.shareholders = []

    def calculate_earnings(self, rand_outcome, day):
        '''
        rand_outcome is calculated by the correlation_matrix from `simulation_manager`.
        The actual outcome should be passed to the function
        '''

        prev_earning = self.earnings.iloc[-1]
        new_earning = prev_earning * (1 + rand_outcome)
        self.earnings.loc[day] = new_earning
        self.cash += new_earning

        return

    def subscribe(self, shareholder):
        '''
        will add `shareholder` to `self.shareholders`
        '''
        self.shareholders.append(shareholder)

    def unsubscribe(self, shareholder):
        '''
        will remove `shareholder` to `self.shareholders`
        '''
        self.shareholders.remove(shareholder)

    def pay_dividends(self):
        total_dividends = self.cash * self.yield_policy
        self.cash -= total_dividends

        for agent in self.shareholders:
            # qty = agent.portfolio.assets[self]
            agent.receive_dividends(self)
            # div_per_share * qty
