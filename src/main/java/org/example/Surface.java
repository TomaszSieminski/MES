package org.example;

public class Surface {
    private final double[][] N;

    public Surface(int numPoints) {
        this.N = new double[numPoints][4];
    }

    public double[][] getN() {
        return N;
    }
}
