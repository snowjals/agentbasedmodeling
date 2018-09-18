package model_1_0;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Market {

	private Portfolio marketPortfolio;
	private Map<Integer,List<Order>> orderbook = new HashMap<>();
	private int currentStep;

	private int nAgents;
	
	public Market(int nAgents, Portfolio initialMarketPortfolio) {
		this.nAgents = nAgents;
		marketPortfolio = initialMarketPortfolio;
	}
	
	
	
	public void addOrders(int step, List<Order> orders) {
		orderbook.put(step, orders);
	}
	
	private void setCurrentStep(int newStep) {
		currentStep = newStep;
	}
	
	public Portfolio getPortfolio() {
		return marketPortfolio; 
	}
	
	
	public List<Order> getAllOrdersOnStep(int step) {
		return orderbook.get(step);
	}
	
	
	public List<Order> getOrders(int step, Stock stock){
		if (orderbook.get(step) == null) {
			System.out.println("No history for step " + step);
			return new ArrayList<Order>();
		}
		return orderbook.get(step).stream().filter(order -> order.getStock() == stock).collect(Collectors.toList());
	}


	public int getStep() {
		return currentStep;
	}

	public void updatePrices(List<Order> orders, int newStep) {
		setCurrentStep(newStep);
		addOrders(currentStep, orders);
		
		for (Stock stock : marketPortfolio.getStocks()) {
			List<Order> relevantOrders = getOrders(newStep,stock);
			updatePrice(stock, relevantOrders);
		}
	}



	private void updatePrice(Stock stock, List<Order> orders) {
		int netOrderImpact = 0;
		netOrderImpact += orders.stream().mapToInt(order -> order.getQuantity()).sum();
		
		double impact = netOrderImpact / (stock.getLambda() * nAgents);
		stock.addPrice(stock.getLastClose() * Math.exp(impact));
	}
	
	
}
