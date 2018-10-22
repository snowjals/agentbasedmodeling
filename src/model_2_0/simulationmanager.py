import numpy as np
from tqdm import tqdm
import json
import test

from agentgenerator import AgentGenerator
from company import Company
from timestamp import Timestamp
from stock import Stock
from orderbook import Orderbook
from exchange import Exchange
from portfolio import Portfolio
from companygenerator import CompanyGenerator


class Simulationmanager:
    def __init__(self, n_days, n_steps_per_day, asset_config_path, agent_config_path):
        self.n_days = n_days
        self.n_steps_per_day = n_steps_per_day

        initial_shares_per_agent = 10
        n_agents = AgentGenerator.n_agents(agent_config_path)
        print(n_agents)

        self.companies = CompanyGenerator.generate_companies(n_companies=10, n_sectors=3)
        self.tickers = [each.ticker for each in self.companies]
        # self.tickers = 'EQNR DNO AKER MHG NRS LSG'.split(' ')
        # self.companies = []
        # for ticker in self.tickers:
        #     comp = Company(ticker=ticker,
        #                    n_shares=initial_shares_per_agent * n_agents,
        #                    cash=100 * initial_shares_per_agent * n_agents,
        #                    yield_policy=0.10)
        #     self.companies.append(comp)

        self.assets = [Stock(comp) for comp in self.companies]

        self.agents = AgentGenerator.generate(agent_config_path, self.assets, verbose=True)
        n_agents = len(self.agents)
        for agent in self.agents:
            for stock in self.assets:
                agent.portfolio.assets[stock] = initial_shares_per_agent

        self.cov_matrix = test.generate_corr_matrix(len(self.tickers), 2, 0.2)
        self.weights = np.ones(len(self.tickers))
        self.weights = self.weights / self.weights.size

        self.book = Orderbook([], [])

        # self.assets = ...

        self.timestamp = Timestamp(0, 0)

        self.market_portfolio = Portfolio.empty_portfolio(self.assets)
        self.exchange = Exchange(self.agents, self.market_portfolio, n_steps_per_day)

        self.history = []

    def realize_earnings(self):
        realizations = np.random.normal(0, np.matmul(self.cov_matrix, self.weights))
        self.exchange.realizations = {k: v for (k, v) in
                                      zip(self.companies, realizations)}

    def simulate(self, logname='/tmp/output.log'):
        for day in tqdm(range(self.n_days - self.timestamp.day)):
            self._simulate_day(day)

        with open(logname, 'w') as f:
            f.write(json.dumps(self.history))

    def _simulate_day(self, day):
        if (day % 68 == 0) and (day > 0):
            print('realizing earnings')
            self.realize_earnings()

        self.exchange.start_of_day(day)

        for step in range(self.n_steps_per_day):
            self._simulate_step(day, step)
        self.exchange.end_of_day(day)
        orderbook_data = self.exchange.orderbook_dumps()
        self.history = self.history + orderbook_data

    def _simulate_step(self, day, step):
        self.timestamp = Timestamp(day, step)

        self.exchange.timestamp = self.timestamp
        for each in self.agents:
            each.update_portfolio(self.exchange)

    def write_log(self, fname, verbose=True):
        with open(fname, 'w+') as f:
            json.dump(self.history, f)
            if verbose: print(f'Histroy written to {fname}')
