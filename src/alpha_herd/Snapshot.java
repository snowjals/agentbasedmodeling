package alpha_herd;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.google.gson.Gson;

@SuppressWarnings("unused")
public class Snapshot {

	private int step;
	private double price;
	private List<Integer> clusters = new ArrayList<Integer>();
	private int nAgents;
	
	
	public Snapshot() {
		
	}
	
	public Snapshot step(int step) {
		this.step = step;
		return this;
	}
	
	public Snapshot price(double price) {
		this.price = price;
		return this;
	}
	
	public Snapshot clusters(List<Integer> clusters) {
		this.clusters = clusters;
		return this;
	}
	
	public Snapshot nAgents(int nAgents) {
		this.nAgents = nAgents;
		return this;
	}
	
	public String toJson() {
		Gson gson = new Gson();
		return gson.toJson(this).toString();
	}
	
	
	public static void main(String[] args) {
		Snapshot snapshot = new Snapshot();
		snapshot.price(100).clusters(new ArrayList<>(Arrays.asList(10,20))).step(2).nAgents(100);
		System.out.println(snapshot.toJson());
	}
	
}
