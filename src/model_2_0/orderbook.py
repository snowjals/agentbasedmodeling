import numpy as np


class Orderbook:
    def __init__(self, highest_bid, lowest_ask, buy_orders=[], sell_orders=[]):
        self.buy_orders = buy_orders
        self.sell_orders = sell_orders
        self.completed_orders = []

        self.highest_bid = highest_bid
        self.lowest_ask = lowest_ask

    def submit(self, order, try_to_match=False):
        '''
        order: instance of order.
        '''

        if order.is_buy():
            if self.lowest_ask > order.bid:
                self.buy_orders.append(order)
                self.highest_bid = max(self.highest_bid or 0, order.bid)
                return
            if try_to_match:
                self.match_buy_order(order)
            else:
                self.buy_orders.append(order)

        else:  # I sell
            if self.highest_bid < order.ask:
                self.sell_orders.append(order)
                self.lowest_ask = min(self.lowest_ask or np.inf, order.ask)
                return
            if try_to_match:
                self.match_sell_order(order)
            else:
                self.sell_orders.append(order)
                # self.match_sell_order(order)

    def match_sell_order(self, order):
        def sort_key(order):
            return (-order.bid, order.submitted_timestamp.step)

        self.buy_orders.sort(key=sort_key)
        self._match_order(order, self.buy_orders)

    def match_buy_order(self, order):
        def sort_key(order):
            return (order.ask, order.submitted_timestamp.step)

        self.sell_orders.sort(key=sort_key)
        self._match_order(order, self.sell_orders)

    @staticmethod
    def will_transact(order1, order2):
        '''
        Returns True if a match between `order1` and `order2` is possible
        '''

        if order1.is_buy():
            return order1.bid >= order2.ask
        elif order2.is_buy():
            return order2.bid >= order1.ask

    def _match_order(self, order, matches):
        '''
        order: Order-instance. The one we would like to match with
        matches: list of Order-instances. The ones we match with.

        This method will successively match `order` until it is either
        completed or there are no more matches to match the order with.
        '''

        match = None
        while (len(matches) > 0) and (not order.is_completed()) and Orderbook.will_transact(matches[0], order):
            match = matches.pop(0)
            if order.is_completed():
                import ipdb;ipdb.set_trace()
            if match.is_completed():  import ipdb;ipdb.set_trace()

            if not Orderbook.will_transact(order, match):
                matches.append(match)  # put it back...
                return

            realized_price = match.get_price()
            timestamp = match.submitted_timestamp
            quantity = min(match.quantity, order.quantity)
            order = self.order_execute(order, realized_price, quantity, timestamp)
            match = self.order_execute(match, realized_price, quantity, timestamp)

        if not order.is_completed():
            self.submit(order)
        if match is not None and (not match.is_completed()) and  match.quantity > 0:
            self.submit(match)
            # matches.append(match)

    def order_execute(self, order, realized_price, quantity, timestamp):
        self.completed_orders.append(order)
        if order.quantity > quantity:
            order = order.partially_execute(realized_price, quantity, timestamp)
            # self.submit(order)
            return order
        else:
            order.execute(realized_price, quantity, timestamp)
            # order.quantity = 0
            return order

    def cancel_all_pending_orders(self):
        for each in self.buy_orders:
            if each.executed_timestamp is not None: import ipdb;ipdb.set_trace()
            cash_delta = each.quantity * each.bid
            each.by.portfolio.update_cash(cash_delta)

        for each in self.sell_orders:
            if each.executed_timestamp is not None: import ipdb;ipdb.set_trace()
            each.by.portfolio.assets[each.asset] += each.quantity

        self.buy_orders = []
        self.sell_orders = []

    def __repr__(self):
        return f'Orderbook w/ {len(self.buy_orders)} buy orders and {len(self.sell_orders)} sell orders'
