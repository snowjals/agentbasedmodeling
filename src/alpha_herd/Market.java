package alpha_herd;
public class Market {

    private int nAgents;
    private double price;
    private double lambda;

    public Market(int nAgents, double price, double lambda) {
        this.nAgents = nAgents;
        this.price = price;
        this.lambda = lambda;
    }

    public void updatePrice(Action action, Agent initiator) {
        int clusterSize = initiator.getClusterSize();
        double impact = action.getAction() * clusterSize;
        price *= Math.exp(impact / (nAgents * lambda));
    }

    public double getPrice() {
        return price;
    }


    public static void main(String[] args) {
        Agent a = new Agent("A");
        Agent b = new Agent("B");
        Agent c = new Agent("C");
        Agent d = new Agent("D");

        a.connect(b);
        b.connect(c);
        c.connect(a);
        d.connect(a);


        Market market = new Market(4,100,1);
        System.out.println(market.getPrice());
        market.updatePrice(new Action(Action.BUY),a);
        System.out.println(market.getPrice());
    }
}
