import numpy as np

from company import Company


class CompanyGenerator:

    def __init__(self):
        pass

    def generate_companies(n_companies, n_sectors):

        ticker_names = [f'CMP{i}' for i in range(n_companies)]
        n_shares = np.random.randint(10_000, 1_000_000, n_companies)
        cash = n_shares * np.random.randint(95, 105, n_companies)
        policy = np.random.uniform(0.00, 0.15, n_companies)
        sectors = np.linspace(0, n_sectors, endpoint=False, dtype=np.int)

        companies = []
        for t, n, c, s, p in zip(ticker_names, n_shares, cash, sectors, policy):
            comp = Company(ticker=t, n_shares=n, cash=c, sector=s, yield_policy=p)
            companies.append(comp)
        return companies
