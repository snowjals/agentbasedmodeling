package alpha_herd;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Agent {


    private List<Agent> connections = new ArrayList<>();
    private String name;

    public Agent(String name) {
        this.name = name;
    }

    public int getClusterSize() {

    return getCluster().size();
    }



    public Set<Agent> getCluster() {
        Set<Agent> visited = new HashSet<>();
        getAgentsInCluster(visited);

        return visited;
    }

    private void getAgentsInCluster(Set<Agent> set) {
       set.add(this);
       for (Agent agent : connections ) {
           if (!set.contains(agent)) {
               agent.getAgentsInCluster(set);
           }
       }

    }


    

    public void connect(Agent agent) {
        if (!connections.contains(agent)) connections.add(agent);
        if (!agent.agentsAreConnected(this)) agent.connect(this);
    }

    private void disconnect(Agent agent) {
        connections.remove(agent);
    }

    public void disconnectCluster() {
        List<Agent> connectionsCopy = new ArrayList<>();
        connectionsCopy.addAll(connections);

        connections.clear();

        connectionsCopy.stream().forEach(agent -> agent.disconnect(this));

        connectionsCopy.stream().forEach(agent -> agent.disconnectCluster());

    }

    public boolean agentsAreConnected(Agent agent) {
        return connections.contains(agent);
    }

    @Override
    public String toString() {

        StringBuilder sb = new StringBuilder();
        connections.stream().forEach(a -> sb.append(a.name).append("\t"));
        return "Agent " + name + " {" +
                "connections=" + sb.toString() +
                '}';
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

        System.out.println(a.getClusterSize());
        a.disconnectCluster();
        System.out.println(a.getClusterSize());


    }

}
