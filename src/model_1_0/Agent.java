package model_1_0;

import java.util.List;
import java.util.stream.Collectors;

public abstract class Agent {

	protected Portfolio portfolio;
	
	public abstract List<Order> updatePortfolio(Market market);

	
	public Agent(Portfolio marketPortfolio) {
		portfolio = new Portfolio(marketPortfolio.getPortfolio().keySet().stream().collect(Collectors.toList()));
	}
	
	protected  void updateStockHolding(Stock stock, int quantity) {
		portfolio.getPortfolio().put(stock, portfolio.getPortfolio().get(stock) + quantity);
	}
	
}
