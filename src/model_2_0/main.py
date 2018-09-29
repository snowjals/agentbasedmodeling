#
import numpy as np
from stock import Stock
from agent import Agent, NoiseAgent
from portfolio import Portfolio
from orderbook import Orderbook
from order import Order
from timestamp import Timestamp
from exchange import Exchange
from agentgenerator import AgentGenerator
from simulationmanager import Simulationmanager
tickers = ['AXA', 'EQNR', 'NHY', 'YARA', 'B2H']
assets = [Stock(each, 100) for each in tickers]
agents = AgentGenerator.generate('agent_config.json', assets)
mng = Simulationmanager(40, 1, None, 'agent_config.json')
mng.simulate()
X = np.array(mng.history)
# plot stuff
plt.ion()
ax = plt.gca()
ax.cla()
for i, stock in enumerate(mng.assets):
    ax.plot(X[:, i], label=stock.ticker)
plt.legend()
mng.agents



Portfolio.empty_portfolio(stocks)
agent = Agent(stocks, 100)
book = Orderbook([], [])
steps = [1,1,2,3,4]
prices = [90, 50, 100, 100, 110]
qty = [1,1,2,1,1]
for s,p,q in zip(steps, prices, qty):
    ts = Timestamp(1, step)
    order = Order.ask(agent, stocks[0], p, q, ts)
    book.submit(order)
my_buy_order = Order.ask(agent, stocks[0], 5, 1, ts)
book.submit(my_buy_order, try_to_match=True)
print('sell orders\n', book.sell_orders)
print('\n\nbuy orders\n', book.buy_orders)


import numpy as np
from stock import Stock
from agent import Agent, NoiseAgent
from portfolio import Portfolio
from orderbook import Orderbook
from order import Order
from timestamp import Timestamp
from exchange import Exchange
n_agents = 10
tickers = ['AXA']
stocks = [Stock(each, 24) for each in tickers]
market_portfolio = Portfolio.empty_portfolio(stocks)
exchange = Exchange(n_agents, market_portfolio)
agents = [NoiseAgent(i, stocks, 1000, 1) for i in range(n_agents)]
OB = exchange.orderbooks[stocks[0]]
for each in agents:
    each.portfolio.assets[stocks[0]] = 10  # all start with 10 stocks
for t in range(10000):
    for i, each in enumerate(agents):
        ts = Timestamp(t, i)
        exchange.timestamp = ts
        each.update_portfolio(exchange)
    OB.cancel_all_pending_orders()
    tot_cash = sum(agent.get_available_funds() for agent in agents)
    tot_cash = np.rint(tot_cash)
    if tot_cash != 1000 * n_agents: import ipdb;ipdb.set_trace()
    for each in stocks:
        completed_orders = exchange.orderbooks[each].completed_orders
        if len(completed_orders) > 1:
            last_close = completed_orders[-1].executed_price
        else:
            last_close = each.prices[-1]
        each.prices.append(last_close)
        exchange.orderbooks[each].cancel_all_pending_orders()
    tot_cash = sum(agent.get_available_funds() for agent in agents)
    print(f'Day {t} -- got cash {tot_cash} and {stocks[0]}\n\n')


plt.ion()
Y = stocks[0].prices
plt.plot(np.arange(len(Y)), Y)
