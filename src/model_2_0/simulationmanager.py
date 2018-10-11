from agentgenerator import AgentGenerator
from timestamp import Timestamp
from stock import Stock
from orderbook import Orderbook
from exchange import Exchange
from portfolio import Portfolio
from tqdm import tqdm
import json


class Simulationmanager:
    def __init__(self, n_days, n_steps_per_day, asset_config_path, agent_config_path):
        self.n_days = n_days
        self.n_steps_per_day = n_steps_per_day

        self.tickers = ['AXA',]
        # self.tickers = ['AXA', 'B2H']
        self.assets = [Stock(each, 100) for each in self.tickers]  # 100 in start price
        self.book = Orderbook([], [])

        # self.assets = ...
        self.agents = AgentGenerator.generate(agent_config_path, self.assets, verbose=True)

        for agent in self.agents:
            for stock in self.assets:
                agent.portfolio.assets[stock] = 100
                pass

        self.timestamp = Timestamp(0, 0)

        self.market_portfolio = Portfolio.empty_portfolio(self.assets)
        self.exchange = Exchange(self.agents, self.market_portfolio)

        self.history = []

    def simulate(self, logname='/tmp/output.log'):
        for day in tqdm(range(self.n_days - self.timestamp.day)):
            self._simulate_day(day)
            close = [each.get_last_price() for each in self.assets]

        with open(logname, 'w') as f:
            f.write(json.dumps(self.history))

    def _simulate_day(self, day):
        self.exchange.start_of_day()  # yaawn
        for step in range(self.n_steps_per_day):
            self._simulate_step(day, step)
        self.exchange.end_of_day()  # ding ding ding
        orderbook_data = self.exchange.orderbook_dumps()
        # import ipdb; ipdb.set_trace()
        self.history = self.history + orderbook_data
        # self.history.append(orderbook_data)

    def _simulate_step(self, day, step):
        self.timestamp = Timestamp(day, step)

        self.exchange.timestamp = self.timestamp
        for each in self.agents:
            each.update_portfolio(self.exchange)
