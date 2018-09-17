package model_1_0;

import java.util.ArrayList;
import java.util.List;

public class NoiseAgent extends Agent{

	private double k;
	private int theta;
	private int H;
	private double tradingIntensity;

	public NoiseAgent(Portfolio marketPortfolio,double k, int theta, int H, double tradingIntensity) {
		super(marketPortfolio);
		this.k = k;
		this.theta = theta;
		this.H = H;
		this.tradingIntensity = tradingIntensity;
	}

	@Override
	public List<Order> updatePortfolio(Market market) {
		List<Order> orders = new ArrayList<>();	

		int nStep = market.getStep();
		
		for (Stock stock : portfolio.getStocks()) { 
			List<Order> relevantOrders = market.getOrders(nStep, stock);
			
			double turnover = Utils.getTurnover(relevantOrders, stock.getLastClose());
			double volatility_theta = Utils.volatility(stock, theta);
			double volatility_H = Utils.volatility(stock, H);
			
			int upper = (int) (turnover * k);
			if (upper == 0) continue;
			
			int quantity = Utils.getRandomUniform(0, upper);
			double z = Utils.getRandomNormal(0, volatility_theta);
			
			if (Math.abs(z) >= tradingIntensity * volatility_H) {
				quantity = (int) Math.round(quantity * k * Math.signum(z)); // if positive -> long, negative -> short 
				
				orders.add(new Order(stock, quantity));
				updateStockHolding(stock, quantity);
				
			} else {
				quantity = 0;
			}
			
			
			
					
		}
		return orders;
	}

}
