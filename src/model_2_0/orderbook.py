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

        if try_to_match:
            # first try to match -- if no match is found, then
            # call `self.submit` with `try_to_match=False`
            self.match_order(order)
            return

        if order.is_buy():
            self.buy_orders.append(order)
        else:
            self.sell_orders.append(order)
        self._update_max_bid_min_ask(order.bid or order.ask)

    def match_order(self, order):
        opposite_orders = self.sell_orders if order.is_buy() else self.buy_orders

        sort_key = None
        if order.is_buy():
            sort_key = lambda x: (x.ask, x.submitted_timestamp.step)  # noqa
        else:
            sort_key = lambda x: (-x.bid, x.submitted_timestamp.step)  # noqa

        opposite_orders.sort(key=sort_key)
        self._match_order(order, opposite_orders)

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

            if not Orderbook.will_transact(order, match):
                self.submit(match)  # put it back
                return

            realized_price = match.get_price()
            timestamp = match.submitted_timestamp
            quantity = min(match.quantity, order.quantity)
            order = self.order_execute(order, realized_price, quantity, timestamp)
            match = self.order_execute(match, realized_price, quantity, timestamp)
            if order.is_completed():
                if not match.is_completed():
                    self.submit(match)
                break

        if not order.is_completed():
            self.submit(order)

    def order_execute(self, order, realized_price, quantity, timestamp):
        self.completed_orders.append(order)
        if order.quantity > quantity:
            order = order.partially_execute(realized_price, quantity, timestamp)
            return order
        else:
            order.execute(realized_price, quantity, timestamp)
            # import ipdb;ipdb.set_trace()
            return order

    def cancel_all_pending_orders(self):
        for each in self.buy_orders:
            cash_delta = each.quantity * each.bid
            each.by.portfolio.update_cash(cash_delta)

        for each in self.sell_orders:
            each.by.portfolio.assets[each.asset] += each.quantity

        self.buy_orders = []
        self.sell_orders = []

    def _update_max_bid_min_ask(self, default_value):
        '''
        Determination of highest bid:
            * if there are currently active orders, choose the highest one
            * otherwise, choose the most recent buy order that is completed
            * otherwise, use the default `self.highest_bid` as reference.

        Determination of lowest ask:
            * If there are currently active orders, choose the lowest one
            * Otherwise, choose the most recent sell order that is completed
            * Otherwise, use the default `self.lowest_ask` as reference.

        returns None
        '''
        if len(self.buy_orders) > 0:
            self.highest_bid = max(self.buy_orders, key=lambda x: x.bid).bid
        elif len(self.completed_orders) > 0:
            order = self.completed_orders[-1]
            self.highest_bid = order.executed_price
        else:
            self.highest_bid = default_value

        if len(self.sell_orders) > 0:
            self.lowest_ask = min(self.sell_orders, key=lambda x: x.ask).ask
        elif len(self.completed_orders) > 0:
            order = self.completed_orders[-1]
            self.lowest_ask = order.executed_price
        else:
            self.lowest_ask = default_value

    def get_bid_ask(self, asset):
        '''
        returns (highest_bid, lowest_ask) of a given asset.
        '''
        return self.highest_bid, self.lowest_ask

    def get_last_completed(self, err_raise=False):
        if len(self.completed_orders) == 0:
            if not err_raise:
                return 0
            else:
                raise ValueError('No completed orders available for this stock')
        return self.completed_orders[-1].executed_price

    def __repr__(self):
        return f'Orderbook w/ {len(self.buy_orders)} buy orders and\
                {len(self.sell_orders)} sell orders'
