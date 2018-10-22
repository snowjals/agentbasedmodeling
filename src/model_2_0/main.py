#
import numpy as np  # noqa
import pandas as pd  # noqa
import matplotlib.pyplot as plt

# from company import Company
# from stock import Stock
# from agent import Agent, NoiseAgent
# from portfolio import Portfolio
# from orderbook import Orderbook
# from order import Order
# from timestamp import Timestamp
# from exchange import Exchange
# from agentgenerator import AgentGenerator
from simulationmanager import Simulationmanager

plt.ion()

n_days = 300
periods_per_day = 10
mng = Simulationmanager(n_days, periods_per_day, None, 'agent_config.json')
agents = mng.agents

mng.simulate()

stocks = mng.market_portfolio.get_stocks()

prices = np.vstack([e.prices for e in stocks]).T
names = [e.company.ticker for e in stocks]

for p, n in zip(prices.T, names):
    plt.plot(p, label=n)
plt.legend()

stocks[0].describe()

# import stock
# adj_close = stocks[0].get_adj_closing_prices()
# 
# fig, axes = plt.subplots(1, 1)
# # axes= axes.flatten()
# 
# axes.plot(adj_close)

write = True
if write:
    mng.write_log('/tmp/simulationlog.json')
