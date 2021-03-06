package model_1_0;

import java.util.ArrayList;
import java.util.List;

public class TrendAgent extends Agent {

	
	private double epsilon;
	private double c;
	private int theta;

	public TrendAgent(Portfolio marketPortfolio, double initialWealth, int theta, double c, double epsilon) {
		super(marketPortfolio, initialWealth);
		this.theta = theta;
		this.c = c;
		this.epsilon = epsilon;
	}
	
	@Override
	public List<Order> updatePortfolio(Market market) {
		List<Order> orders = new  ArrayList<>();
		
		for (Stock stock : market.getPortfolio().getStocks()) {
            int historyPrice = stock.getPrices().size();
			if (stock.getPrices().size() < theta + 1 ) { 
				continue;
			}

            int theta = Math.min(historyPrice, this.theta);
			
			double currentPrice = stock.getLastClose();	
			double currentLogPrice = Math.log(currentPrice);
			double referencePrice = Math.log(stock.getPrices().get(stock.getPrices().size() - (theta + 1)));

			if (Math.abs(currentLogPrice - referencePrice) >= epsilon) {
                int quantity = Math.max(1, (int) Math.round(c * (currentLogPrice - referencePrice) - portfolio.getX(stock)));
				if (quantity != 0) {
					if (! sufficientFunds(quantity,currentPrice)) {
						quantity = (int) adjustQuantity(currentPrice);
					}
					orders.add(new Order(stock,quantity, this));
					updateAssetHolding(stock, quantity);
				}
				
			}
			
		}
		
		
		return orders;
	}

	

}
