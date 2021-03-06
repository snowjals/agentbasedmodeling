package model_1_0;
import java.util.ArrayList;
import java.util.List;

public class SimulationManager {

	private int currentStep;
	private int nSteps;
	private int nNoiseAgents;
	private int nTrendAgents;
	private double k;
	private int H;
	private double tradingIntensity;
	private List<Agent> agents = new ArrayList<Agent>();
	private Market market;
	
	
	
	public SimulationManager(int nSteps, int nNoiseAgents, int nTrendAgents, double k, int H,
			double tradingIntensity) {
		this.nSteps = nSteps;
		this.nNoiseAgents = nNoiseAgents;
		this.nTrendAgents = nTrendAgents;
		this.k = k;
		this.H = H;
		this.tradingIntensity = tradingIntensity;
	
		init();
		
	}

	private Portfolio initialMarketPorfolio() {
		double lambda = 25;
		Stock stock = new Stock("VIX",100,lambda);
		List<Asset> stocks = new ArrayList<Asset>();
		stocks.add(stock);
		Portfolio marketPortfolio = new Portfolio(stocks);
		return marketPortfolio;
	}

	private void init() {
		initializeMarket();
		initializeAgents();
	}


	private void initializeMarket() {
		Portfolio initialMarketPortfolio = initialMarketPorfolio();
		this.market = new Market(nNoiseAgents + nTrendAgents,initialMarketPortfolio);
		
	}




	private void initializeAgents() {
		initializeNoiseAgents();
		initializeTrendAgents();
	
	}


	private void initializeTrendAgents() {
		double initialWealth = 100000;
		
		int theta = 30;
		double c = 1.2;
		double epsilon = 0.05;
		
		for (int i = 0; i < nTrendAgents; i++) {
			Agent agent = new TrendAgent(market.getPortfolio(), initialWealth ,theta, c, epsilon); // TODO fix random variables
			agents.add(agent);
		}
		
		
	}


	private void initializeNoiseAgents() {
		double initialWealth = 100000;
		
		int theta = 5; // TODO;
		for (int i = 0; i < nNoiseAgents; i++) {
			Agent agent = new NoiseAgent(market.getPortfolio(), initialWealth,k,theta,H,tradingIntensity);
			agents.add(agent);
		}
		
	}
	
	public void simulate() {
		kickStartSystem();
		
		for (int i = currentStep; i < nSteps; i++) {
			doStep();
			// System.out.println("Step: " + currentStep + " Price: " + market.getPortfolio().getStocks().get(0).getPrices().get(market.getPortfolio().getStocks().get(0).getPrices().size() - 1));
			currentStep++;
		}
		
	}
	
	private void kickStartSystem() {
		
		for (int i = 0; i < 10; i++) {
			List<Order> orderBook = new ArrayList<>();
			orderBook.add(new Order(market.getPortfolio().getStock("VIX"),1, null));
			for (Agent agent : agents) {
				orderBook.addAll(agent.updatePortfolio(market));
			}
			market.updatePrices(orderBook, currentStep);
		
			// System.out.println("Step: " + currentStep + " Price: " + market.getPortfolio().getStocks().get(0).getPrices().get(market.getPortfolio().getStocks().get(0).getPrices().size() - 1));
			currentStep++;
	
		}
		
	}

	private void doStep() {
		List<Order> orderBook = new ArrayList<>();
		for (Agent agent : agents) {
			orderBook.addAll(agent.updatePortfolio(market));
		}

		market.updatePrices(orderBook, currentStep);
        double currPrice = market.getPortfolio().getStock("VIX").getLastClose();
        System.out.println("in step " + this.currentStep +  ", price is " + currPrice + " and orderbook is this: \n" + orderBook);
        System.out.println("\n");


		
	}
	
	
	public static void main(String[] args) {
		SimulationManager manager = new SimulationManager(100, 30, 30, 1/200, 10, 1.25);
		manager.simulate();
	}
	
	
}
