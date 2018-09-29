from asset import Asset


class Stock(Asset):
    def __init__(self, ticker, price):
        '''
        ticker: string, the ticker symbol. Example: 'ticker'
        price: The initial price. It is stored in `self.prices`
        '''

        self.ticker = ticker
        self.prices = [price]

    def get_last_price(self):
        return self.prices[-1]

    def add_price(self, new_price):
        self.prices.append(new_price)
        return

    def __repr__(self):
        return f'[Stock {self.ticker}@{self.get_last_price()}]'
