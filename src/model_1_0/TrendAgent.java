package model_1_0;

import java.util.ArrayList;
import java.util.List;

public class TrendAgent extends Agent {

	
	private double epsilon;
	private double c;
	private int theta;

	public TrendAgent(Portfolio marketPortfolio,int theta, double c, double epsilon) {
		super(marketPortfolio);
		this.theta = theta;
		this.c = c;
		this.epsilon = epsilon;
	}
	
	@Override
	public List<Order> updatePortfolio(Market market) {
		List<Order> orders = new  ArrayList<>();
		
		for (Stock stock : market.getPortfolio().getStocks()) {
			if (stock.getPrices().size() <= theta) {  //TODO
				continue;
			}
				
			double currentLogPrice = Math.log(stock.getPrices().get(stock.getPrices().size() - 1));
			double referencePrice = Math.log(stock.getPrices().get(stock.getPrices().size() - (theta + 1)));
			
			if (Math.abs(currentLogPrice - referencePrice) >= epsilon) {
				int quantity = (int) Math.round(c * (currentLogPrice - referencePrice) - portfolio.getX(stock));
				if (quantity != 0) {
					orders.add(new Order(stock,quantity));
					updateStockHolding(stock, quantity);
				}
				
			}
			
		}
		
		
		return orders;
	}

	

}
