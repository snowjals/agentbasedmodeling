package model_1_0;

public class Order {

	private int quantity;
	private Stock stock;

	public Order(Stock stock, int quantity) {
		this.stock = stock;
		this.quantity = quantity;
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
	
	

}
