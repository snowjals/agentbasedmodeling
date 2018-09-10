public class Action {

public static final int BUY = 1;
    public static final int HOLD = 0;
    public static final int SELL = -1;
    private final int action;


    public Action(int action) {
        this.action = action;
    }

    public int getAction() {
        return action;
    }





}
