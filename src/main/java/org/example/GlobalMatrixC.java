package org.example;

public class GlobalMatrixC {
    private final double[][] globalMatrixC;
    private final GlobalData globalData;

    public GlobalMatrixC(GlobalData globalData) {
        this.globalData = globalData;
        this.globalMatrixC = new double[globalData.getnN()][globalData.getnN()];
    }

    public void calculateGlobalMatrixC(Element element, double[][] localC) {
        int[] nodes = element.getElements();
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                globalMatrixC[nodes[i] - 1][nodes[j] - 1] += localC[i][j];
            }
        }
    }

    public double[][] getGlobalMatrixC() {
        return globalMatrixC;
    }

    public void printGlobalMatrixC() {
        System.out.println("\nGlobal Matrix C:");
        for (double[] row : globalMatrixC) {
            for (double val : row) {
                System.out.printf("| %8.5f ", val);
            }
            System.out.println("|");
        }
    }
}