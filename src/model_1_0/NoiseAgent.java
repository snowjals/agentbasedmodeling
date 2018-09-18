package model_1_0;

import java.util.ArrayList;
import java.util.List;


public class NoiseAgent extends Agent{

	private double k;
	private int theta;
	private int H;
	private double tradingIntensity;

	public NoiseAgent(Portfolio marketPortfolio,double initialWealth, double k, int theta, int H, double tradingIntensity) {
		super(marketPortfolio,initialWealth);
		this.k = k;
		this.theta = theta;
		this.H = H;
		this.tradingIntensity = tradingIntensity;
	}

	@Override
	public List<Order> updatePortfolio(Market market) {
		List<Order> orders = new ArrayList<>();	

		int currentStep = market.getStep();

		for (Stock stock : portfolio.getStocks()) { 
			List<Order> relevantOrders = market.getOrders(currentStep-1, stock);


			double turnover = Utils.getTurnover(relevantOrders, stock.getLastClose());
			double volatility_theta = Utils.volatility(stock, theta);
			double volatility_H = Utils.volatility(stock, H);

            if (currentStep == 10) {
                System.out.println("relevant orders: "+ relevantOrders);
                System.out.println("turnover, vols: " + turnover + ", " + volatility_theta + ", " + volatility_H);
            }

            // k is too small --> upper limit is zero
            int upper= Math.max(1, (int)(turnover * k));
			// int upper = (int) (turnover * k);
            //System.out.println(turnover + ", " + k + ", " + turnover*k);
            if (upper == 0) {
                System.out.println("upper is zero -- no trade for noise");
                continue;
            } 

			double currentPrice = stock.getLastClose();
			int quantity = Utils.getRandomUniform(0, upper);
			double z = Utils.getRandomNormal(0, volatility_theta);

			if (Math.abs(z) >= tradingIntensity * volatility_H) {
                int sign = 1;
                if (z < 0) {
                    sign = -1;
                }
                quantity = (int) Math.max(quantity * k, 1) * sign;

				if (quantity != 0) {
					if (! sufficientFunds(quantity,currentPrice)) {
						quantity = (int) adjustQuantity(currentPrice);
					}
				}

				orders.add(new Order(stock, quantity, this));
				updateAssetHolding(stock, quantity);

			} else {
				quantity = 0;
			}




		}
		return orders;
	}

}
