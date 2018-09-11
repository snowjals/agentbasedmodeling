package alpha_herd;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.*;

import com.google.gson.Gson;

public class SimulationManager {


	private static final String RESULT_FILE = "result.json";
	private double probabilityOfAction;
	private int currentStep;
	private int steps;
	private Market market;
	private int nAgents;

	private List<Agent> agents = new ArrayList<>();

	private List<Snapshot> snapshots = new ArrayList<>();

	public SimulationManager(int nAgents,double price, double lambda, int steps, double probabilityOfAction) {
		this.nAgents = nAgents;
		this.probabilityOfAction = probabilityOfAction;
		this.steps = steps;
		this.market = new Market(nAgents,price,lambda);

		init();
	}

	private void init() {
		for (int i = 0; i < nAgents; i++) {
			Agent agent = new Agent("00" + i);
			agents.add(agent);
		}
	}

	private Agent selectAgent() {
		Random random = new Random();
		return agents.get(random.nextInt(agents.size()));
	}

	private Action generateAction() {
		Random random = new Random();
		double draw = random.nextDouble();

		int action = 0;
		if (draw <= probabilityOfAction){
			action = random.nextInt(2) * 2 - 1;
		}

		return new Action(action);
	}

	private void doStep(){
		Agent initiator = selectAgent();
		Action action = generateAction();

		market.updatePrice(action,initiator);

		if (action.getAction() == Action.BUY || action.getAction() == Action.SELL){
			initiator.disconnectCluster();
		} else {
			connectToRandomAgent(initiator);
		}
		createSnapshot();
		//System.out.println("Action " + action.getAction() + " \t Price " + market.getPrice());
		currentStep++;
	}

	private void connectToRandomAgent(Agent initiator) {
		List<Agent> agentsInCluster = new ArrayList<>();
		agentsInCluster.addAll(initiator.getCluster());

		List<Agent> candidates = new ArrayList<>();
		candidates.addAll(agents);
		candidates.removeAll(agentsInCluster);

		if (!candidates.isEmpty()) {
			Random random = new Random();
			initiator.connect(candidates.get(random.nextInt(candidates.size())));
		} else {
			System.out.println("Found no candidates. Probable reason: cluster is full.)");
		}

	}

	public void simulate() {
		while (currentStep < steps) {
			doStep();
		}

	}

	public double calculateHerdingDegree(){
		return (1/probabilityOfAction - 1);
	}

	private void createSnapshot() {
		Snapshot snapshot = new Snapshot();
		snapshot.price(market.getPrice()).step(currentStep).nAgents(nAgents).clusters(getClusters());
		snapshots.add(snapshot);
	}

	private void saveResult() throws FileNotFoundException {
		PrintWriter writer = new PrintWriter(new File(RESULT_FILE));
		Gson gson = new Gson();
		String output = gson.toJson(snapshots);
		writer.println(output);
		writer.flush();
		writer.flush();
	}

	private List<Integer> getClusters() {
		Set<Agent> pool = new HashSet<Agent>();
		List<Integer> clusters = new ArrayList<Integer>();

		pool.addAll(agents);

		for (Agent agent : agents) {
			if (pool.contains(agent)) {
				Set<Agent> aCluster = agent.getCluster();
				if (aCluster.size() > 1) clusters.add(aCluster.size());
				pool.removeAll(aCluster);
			}
		}

		return clusters;
	}

	public static void main(String[] args) {
		SimulationManager manager = new SimulationManager(1000,100,1,10000, 0.1);
		manager.simulate();
		try {
			manager.saveResult();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}



	}

}
