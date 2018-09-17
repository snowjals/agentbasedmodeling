package model_1_0;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Portfolio {

	
	private Map<Stock, Integer> portfolio = new  HashMap<>();
	

	public Portfolio(List<Stock> stocks) {
		for (Stock stock : stocks) {
			portfolio.put(stock, 0); // TODO add shares outstanding
		}
	}

	public Map<Stock,Integer> getPortfolio() {
		return portfolio;
	}
	
	public List<Stock> getStocks() {
		return portfolio.keySet().stream().collect(Collectors.toList());
	}
	
	public Stock getStock(String ticker) {
		for (Stock stock : portfolio.keySet()) {
			if (stock.getTicker().equals(ticker)) {
				return stock;
			}
		}
			
			return null;
	}
	
	public int getX(Stock stock) {
		return (portfolio.containsKey(stock) ? portfolio.get(stock) : 0);
	}
	
}
