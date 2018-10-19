import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import stats

from asset import Asset


class Share():
    def __init__(self, company):
        '''
        ticker: string, the ticker symbol. Example: 'ticker'
        price: The initial price. It is stored in `self.prices`
        '''

        self.company = company
        self.ticker = company.ticker

        # initial price
        self.prices = [company.cash / company.n_shares]

        self.div_period = 68  # days
        self.earnings_period = 68  # days

    def get_last_price(self):
        return self.prices[-1]

    def add_price(self, new_price):
        self.prices.append(new_price)
        return

    def get_last_div_per_share(self):
        dividend_payout = self.company.dividends.iloc[-1]
        n_shares = self.company.n_shares

        return dividend_payout / n_shares

    def is_dividend_day(self, day):
        return (day > 0) and (day % self.div_period == 0)

    def is_earnings_day(self, day):
        return (day > 0) and (day % self.earnings_period == 0)

    def pay_dividends(self, day):
        total_dividends = self.company.cash * self.company.yield_policy
        self.company.dividends.loc[day] = total_dividends
        self.company.cash -= total_dividends

        div_per_share = self.get_last_div_per_share()
        print(f'Company {self.ticker} payin\' out {total_dividends} :)')
        for agent in self.company.shareholders:
            agent.receive_dividends(self, div_per_share)

    def describe(self):
        P = np.array(self.prices)
        R = np.diff(np.log(P))
        nobs, minmax, mean, variance, skew, kurtosis = stats.describe(R)

        annual_std = np.sqrt(variance / nobs * 250)
        # annual_mean = mean / 250

        print('----- return distribution -----')
        print(f'observations:\t{nobs}')
        print(f'μ\t\t{mean:.3f}')
        print(f'σ\t\t{annual_std:.1f}')
        if input('Plot? [y/n] ').lower() == 'y':
            fig, axes = plt.subplots(1,2)
            axes = axes.flatten()

            axes[0].hist(R, bins=100); axes[0].set_title('return distribution')  # noqa
            axes[1].plot(P); axes[1].set_title('price history')  # noqa
            input()
            # plt.waitforbuttonpress()

    def __repr__(self):
        return f'Share {self.ticker}@{self.get_last_price()}'
