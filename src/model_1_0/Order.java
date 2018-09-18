package model_1_0;

public class Order {

	private int quantity;
	private Stock stock;
    private Agent by;

	public Order(Stock stock, int quantity, Agent by) {
		this.stock = stock;
		this.quantity = quantity;
        this.by = by;
	}

	public int getQuantity() {
		return quantity;
	}

	public void setQuantity(int quantity) {
		this.quantity = quantity;
	}

	public Stock getStock() {
		return stock;
	}

	public void setStock(Stock stock) {
		this.stock = stock;
	}

    public String toString() {
        String agentStr = "";
        if (this.by== null) {
            agentStr = "nullAgent";
        } else {
            agentStr = by.getClass().getSimpleName();
        }
        return "Order " + this.stock.getTicker() + ":" + this.quantity + "by " + agentStr + "\n";
    }
	
	

}
