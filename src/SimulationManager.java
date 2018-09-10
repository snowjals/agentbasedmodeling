import java.util.*;

public class SimulationManager {


    private double probabilityOfAction;
    private int currentStep;
    private int steps;
    private Market market;
    private double nAgents;

    private List<Agent> agents = new ArrayList<>();


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
        System.out.println("Action " + action.getAction() + " \t Price " + market.getPrice());
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


    public static void main(String[] args) {
        SimulationManager manager = new SimulationManager(10,100,-1,100, 0.1);
        manager.simulate();



    }

}
