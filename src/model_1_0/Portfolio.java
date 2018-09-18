package model_1_0;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class Portfolio {

	
	private Map<Asset, Double> portfolio = new  HashMap<>();
	

	public Portfolio(List<Asset> assets) {
		for (Asset asset : assets) {
			portfolio.put(asset, 0.0); // TODO add shares outstanding
		}
	}

	public Map<Asset,Double> getPortfolio() {
		return portfolio;
	}
	
	public List<Stock> getStocks() {
		List<Stock> stocks = new ArrayList<Stock>();
		portfolio.keySet().stream().filter(asset -> asset instanceof Stock).forEach(stock -> {
			if (stock instanceof Stock) {
				stocks.add((Stock) stock);
			}
		});
		return stocks;
	}
	
	public Stock getStock(String ticker) {
		for (Asset asset : portfolio.keySet()) {
			if (asset instanceof Stock && ((Stock) asset).getTicker().equals(ticker)) {
				return (Stock) asset;
			}
		}
			
			return null;
	}
	
	public double getX(Asset asset) {
		return (portfolio.containsKey(asset) ? portfolio.get(asset) : 0.0);
	}

	public void updateCash(double change) {
		Asset cash = portfolio.keySet().stream().filter(asset -> asset instanceof Cash).collect(Collectors.toList()).get(0);
		//  unchecked NPE: the program should crash, i.e no cash object exists for the portfolio
		double currentCash = portfolio.get(cash);
		portfolio.put(cash, currentCash + change);
		
		
		
	}
	
//	public double getFractionInvestedInStocks() {
//		double totalWealth = getTotalWealth();
//		
//	}
	
	
}
