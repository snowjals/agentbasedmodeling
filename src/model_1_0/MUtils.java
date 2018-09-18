package model_1_0;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

public class MUtils {
    public static double max(double n1, double n2) {
        return Math.max(n1, n2);
    }
    public static List<Double> square(List<Double> arr) {
        return arr.stream().map(x -> Math.pow(x, 2)).collect(Collectors.toList());
    }

    public static double mean(List<Double> arr) {
        return arr.stream().mapToDouble(x -> x).average().orElse(0.0);
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
