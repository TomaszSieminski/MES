package org.example;

public class MatrixC {
    private final double[][][] J1;
    private final double[] detJ;
    private final double[][] shapeFunctions;
    private final int npc;
    private double[][][] Cpc;
    private double[][] C;
    private final double[] gaussWeights;
    private double[] calculatedWeights;
    private final int integrationPoints;
    private final double specificHeat;
    private final double density;

    public MatrixC(int integrationPoints, GlobalData globalData, ElementUni elementUni, Jacobian jacobian) {
        this.specificHeat = globalData.getSpecificHeat();
        this.density = globalData.getDensity();
        this.J1 = jacobian.getJ1();
        this.detJ = jacobian.getDetJ();
        GaussQuadratureData gaussQuadratureData = new GaussQuadratureData(integrationPoints);
        this.gaussWeights = gaussQuadratureData.getWeights();
        this.npc = integrationPoints * integrationPoints;
        this.integrationPoints = integrationPoints;

        // Shape functions
        double[] ksiEtaValues = elementUni.getKsiEtaValues();
        this.shapeFunctions = new double[npc][4];
        int idx = 0;
        for (int i = 0; i < integrationPoints; i++) {
            for (int j = 0; j < integrationPoints; j++) {
                shapeFunctions[idx++] = elementUni.calculateShapeFunctions(ksiEtaValues[j], ksiEtaValues[i]);
            }
        }

        calculateWeights();
        calculateMatrixC();
    }

    public double[][] getC() {
        return C;
    }

    private void calculateWeights() {
        int index = 0;
        calculatedWeights = new double[npc];
        for (int i = 0; i < integrationPoints; i++) {
            for (int j = 0; j < integrationPoints; j++) {
                calculatedWeights[index++] = gaussWeights[i] * gaussWeights[j];
            }
        }
    }

    private void calculateMatrixC() {
        int size = shapeFunctions[0].length;
        Cpc = new double[npc][size][size];
        C = new double[size][size];

        for (int p = 0; p < npc; p++) {
            double weight = calculatedWeights[p] * detJ[p];
            for (int i = 0; i < size; i++) {
                for (int j = 0; j < size; j++) {
                    Cpc[p][i][j] = shapeFunctions[p][i] * shapeFunctions[p][j] * specificHeat * density * weight;
                    C[i][j] += Cpc[p][i][j];
                }
            }
        }
    }

    public void printMatrixCpc() {
        for (int p = 0; p < npc; p++) {
            System.out.println("Matrix Cpc" + (p + 1) + ":");
            for (double[] row : Cpc[p]) {
                System.out.print("|");
                for (double value : row) {
                    System.out.printf(" %5.3f ", value);
                }
                System.out.println("|");
            }
            System.out.println();
        }
    }

    public void printMatrixC() {
        System.out.println("Matrix C:");
        for (double[] row : C) {
            System.out.print("|");
            for (double value : row) {
                System.out.printf(" %5.3f ", value);
            }
            System.out.println("|");
        }
    }
}