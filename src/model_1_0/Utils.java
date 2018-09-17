package model_1_0;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;


public class Utils {


	public static List<Double> getLogPrices(Stock stock){
		List<Double> logPrices = new ArrayList<>();
		logPrices.stream().forEach(price -> logPrices.add(Math.log(price)));
		return logPrices;
	}

	public static List<Double> getReturns(Stock stock){
		List<Double> logReturns = new ArrayList<Double>();
		
		if (stock.getPrices().size() > 1) {
			for (int i = 1; i < stock.getPrices().size(); i++) {
				logReturns.add(Math.log(stock.getPrices().get(i) / stock.getPrices().get(i - 1))); 
			}
		}
		
		return logReturns;
		
	}
	
	public static double getTurnover(List<Order> orders, double price) {
		return (price) * (orders.stream().mapToDouble(order -> Math.abs(order.getQuantity())).sum());
	}

	public static double volatility(Stock stock, int timeHorizon) {
		List<Double> logReturns = getReturns(stock);
		List<Double> X = reverse(logReturns).subList(0, Math.min(timeHorizon + 1,logReturns.size()));
		double variance = (logReturns.size() == 0 ? 0 : X.stream().mapToDouble(x -> Math.pow(x, 2)).average().getAsDouble() - Math.pow(X.stream().mapToDouble(d -> d.doubleValue()).average().getAsDouble(),2));
		
		return Math.sqrt(variance);
	}

	/*@Deprecated
	public static List<Double> reverse(List<Double> list) {
		List<Double> newList = new ArrayList<>();
		for (int i = list.size() - 1; i == 0; i--) {
			newList.add(list.get(i));
		}
		return newList;
	}*/
	
	public static <T> List<T> reverse(List<T> list){
		List<T> newList = new ArrayList<>(list);
		Collections.reverse(newList);
		return newList;
	}
	
	
	public static int getRandomUniform(int lower, int upper) {
		Random random = new Random();
		
		return lower + random.nextInt(upper - lower); 
		
	}
	
	public static double getRandomNormal(double mean, double std) {
		Random random = new Random();
		
		return mean + random.nextGaussian() * std;
		
	}


}
