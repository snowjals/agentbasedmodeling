from cash import Cash


class Order:
    def __init__(self, agent, asset, price, quantity, timestamp, order_type, buy):
        if type(asset) == Cash:
            raise ValueError(f'Doesn\'t make sense to buy cash, you retard')

        if quantity <= 0:
            raise ValueError(f'Quantity should be >= 0. Got {quantity}.')

        self.by = agent
        self.asset = asset
        self.quantity = quantity
        self.submitted_timestamp = timestamp
        self.executed_timestamp = None
        self.executed_price = None
        self.executed_quantity = None
        self.order_type = order_type

        if buy:
            self.bid = price
            self.ask = None
        else:
            self.bid = None
            self.ask = price

    @staticmethod
    def bid(agent, asset, price, quantity, timestamp, order_type='limit'):
        return Order(agent, asset, price, quantity, timestamp, order_type=order_type, buy=True)

    @staticmethod
    def ask(agent, asset, price, quantity, timestamp, order_type='limit'):
        return Order(agent, asset, price, quantity, timestamp, order_type=order_type, buy=False)

    def execute(self, realized_price, executed_quantity, timestamp):
        '''
        Updates `self.executed_timestamp`
        '''
        self.executed_timestamp = timestamp
        self.executed_price = realized_price
        self.executed_quantity = executed_quantity
        self.by.update_asset_holdings(self)

    def partially_execute(self, realized_price, quantity, timestamp):
        '''
        Partially executes a given order. This will reduce
        '''
        if quantity >= self.quantity:
            raise ValueError(f'Partially executing order with quantity {quantity} > `self.quantity`\
                    ({self.quantity})')

        self.execute(realized_price, quantity, timestamp)

        order_type = Order.bid if self.is_buy() else Order.ask
        return order_type(self.by,
                          self.asset,
                          self.get_price(),
                          self.quantity - quantity,
                          self.submitted_timestamp,
                          self.order_type)

    def is_completed(self):
        return self.executed_timestamp is not None

    def is_buy(self):
        return self.bid is not None

    def get_price(self):
        return self.bid or self.ask

    def __repr__(self):
        ticker = self.asset.ticker
        type = 'buy' if self.is_buy() else 'sell'
        price = self.bid or self.ask
        return f'{type} order on {ticker}: Q={self.quantity}, P={price}'
