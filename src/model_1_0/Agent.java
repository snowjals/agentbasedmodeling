package model_1_0;

import java.util.List;
import java.util.stream.Collectors;

public abstract class Agent {

	protected Portfolio portfolio;
	protected Cash cash;

	public abstract List<Order> updatePortfolio(Market market);


	public Agent(Portfolio marketPortfolio, double initialWealth) {
		portfolio = new Portfolio(marketPortfolio.getPortfolio().keySet().stream().collect(Collectors.toList()));
		Cash cash = new Cash();
		portfolio.getPortfolio().put(cash, initialWealth);
		this.cash = cash;
	}

	protected  void updateAssetHolding(Asset asset, double quantity) {
		portfolio.getPortfolio().put(asset, portfolio.getPortfolio().get(asset) + quantity);
		if (asset instanceof Stock) {
			double amount = quantity * ((Stock) asset).getLastClose();
			portfolio.updateCash( - amount); // the change is negative for a buy, positive for a sell
			
		} else if (asset instanceof Bond) {
			double amount = quantity * ((Stock) asset).getLastClose();
			portfolio.updateCash( - amount); // see above

		} else if (asset instanceof Cash){
			portfolio.getPortfolio().put(cash, quantity);
		}
	}

	protected boolean sufficientFunds(int quantity, double price) {
		double cashAvailable = portfolio.getX(cash);
		double amount = quantity * price;

		if (cashAvailable >= amount ) {
			return true;
		}
		return false;
	}

	protected double adjustQuantity(double price) {
		double cashAvailable = portfolio.getX(cash);
		return Math.floor(cashAvailable  / price);
	}
}
