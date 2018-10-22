from stock import Stock
# from stock import Stock
from cash import Cash


class Portfolio:
    def __init__(self, assets):
        '''
        assets: list of assets or dictionary of {asset: amount}
            example: [[B2H @100], [NHY @ 48]]
                     {[B2H @100]: 25, [NHY @ 48]: 23.2, Cash: 100}

        Stores `assets` in `self.assets`.

        '''
        self.assets = {}
        if type(assets) == list:
            for each in assets:
                self.assets[each] = 0.0
        elif type(assets) == dict:
            self.assets = assets
        else:
            raise ValueError(f'Expected `assets` to be a list or dictionary. Got {type(assets)}')

        self.bonds = 0
        self.cash = self._get_cash()

    @staticmethod
    def empty_portfolio(assets):
        '''
        Assets: list of stocks or bonds that a portfolio may consist of.

        This method simply makes a new portfolio with a `Cash` asset with quantity 0.
        '''
        if not type(assets) == list:
            raise ValueError(f'`assets` must be list. Got {type(list)}')

        # make a copy
        assets = [each for each in assets]
        assets.append(Cash())

        return Portfolio(assets)

    def get_stocks(self):
        return [each for each in list(self.assets.keys()) if type(each) == Stock]

    def _get_cash(self):
        '''
        returns the cash instance of the portfolio.
        Should usually not be used by the user: use `self.cash` insteead.
        '''
        for k, v in self.assets.items():
            if type(k) == Cash:
                return k

    def update_cash(self, delta):
        '''
        Updates the cash amount available in the portfolio:
            `self.cash = self.cash + delta`

        '''
        return self.set_cash_amount(self.get_cash_amount() + delta)

    def get_cash_amount(self):
        '''
        Returns the amount of cash the portfolio has.
        '''
        return self.assets[self.cash]

    def set_cash_amount(self, amount):
        '''
        Sets `self.assets[self.cash]` to `amount`.
        '''
        self.assets[self.cash] = amount

    def get_stock(self, ticker):
        '''
        Returns the Stock with a given ticker. If no stock
        is found, returns None.

        --
        Example:
            get_stock('AXA') --> [Stock AXA@100]
        '''
        for k, _ in self.assets:
            if type(k) == Stock and k.ticker == ticker:
                return k

    def __repr__(self):
        s = 'Portfolio\n'
        for each in self.assets:
            s += f'{str(each)}\t'
        return s
