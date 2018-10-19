#
import numpy as np  # noqa
import pandas as pd  # noqa
import matplotlib.pyplot as plt

# from company import Company
# from share import Share
# from agent import Agent, NoiseAgent
# from portfolio import Portfolio
# from orderbook import Orderbook
# from order import Order
# from timestamp import Timestamp
# from exchange import Exchange
# from agentgenerator import AgentGenerator
from simulationmanager import Simulationmanager

plt.ion()

n_days = 150
periods_per_day = 10
mng = Simulationmanager(n_days, periods_per_day, None, 'agent_config.json')
agents = mng.agents

mng.simulate()

stocks = mng.market_portfolio.get_stocks()

stocks[0].describe()

write = True
if write:
    mng.write_log('/tmp/simulationlog.json')
