package model_1_0;

import java.util.ArrayList;
import java.util.List;

public class Stock extends Asset {

	private List<Double> prices = new ArrayList<>();
	private String ticker;
	private double lambda;
	
	
	
	
	public Stock(String ticker, double price, double lambda) {
		this.ticker = ticker;
		prices.add(price);
		this.lambda = lambda;
	}
	public List<Double> getPrices() {
		return prices;
	}
	public void setPrices(List<Double> prices) {
		this.prices = prices;
	}
	public String getTicker() {
		return ticker;
	}
	public double getLastClose() {
		return (prices.get(prices.size() - 1) );
	}
	
	public double getLambda() {
		return lambda;
	}
	public void addPrice(double price) {
		prices.add(price);
		
	}
	
	
	
}
