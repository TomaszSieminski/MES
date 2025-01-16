package org.example;

public class GaussSolver {
    private final GlobalData globalData;
    private final double[][] globalMatrixH;
    private final double[] globalP;
    private final double[] temperatures;
    private final int matrixSize;

    public GaussSolver(GlobalData globalData, double[][] matrix, double[] vector) {
        this.globalData = globalData;
        this.matrixSize = globalData.getnN();
        this.globalMatrixH = matrix;
        this.globalP = vector;
        this.temperatures = new double[matrixSize];
    }

    public double[] solve() {
        double[][] A = copyMatrix(globalMatrixH);
        double[] b = globalP.clone();

        for (int i = 0; i < matrixSize - 1; i++) {
            int maxRow = findPivotRow(A, i);
            if (maxRow != i) {
                swapRows(A, b, i, maxRow);
            }

            for (int j = i + 1; j < matrixSize; j++) {
                double factor = A[j][i] / A[i][i];
                for (int k = i; k < matrixSize; k++) {
                    A[j][k] -= factor * A[i][k];
                }
                b[j] -= factor * b[i];
            }
        }

        temperatures[matrixSize - 1] = b[matrixSize - 1] / A[matrixSize - 1][matrixSize - 1];
        for (int i = matrixSize - 2; i >= 0; i--) {
            double sum = 0.0;
            for (int j = i + 1; j < matrixSize; j++) {
                sum += A[i][j] * temperatures[j];
            }
            temperatures[i] = (b[i] - sum) / A[i][i];
        }

        return temperatures;
    }

    private int findPivotRow(double[][] matrix, int col) {
        int maxRow = col;
        double maxValue = Math.abs(matrix[col][col]);

        for (int i = col + 1; i < matrixSize; i++) {
            if (Math.abs(matrix[i][col]) > maxValue) {
                maxValue = Math.abs(matrix[i][col]);
                maxRow = i;
            }
        }
        return maxRow;
    }

    private void swapRows(double[][] matrix, double[] vector, int row1, int row2) {
        double[] tempRow = matrix[row1];
        matrix[row1] = matrix[row2];
        matrix[row2] = tempRow;

        double tempVal = vector[row1];
        vector[row1] = vector[row2];
        vector[row2] = tempVal;
    }

    private double[][] copyMatrix(double[][] original) {
        double[][] copy = new double[matrixSize][matrixSize];
        for (int i = 0; i < matrixSize; i++) {
            System.arraycopy(original[i], 0, copy[i], 0, matrixSize);
        }
        return copy;
    }

    public void printResults() {
        System.out.println("\nCalculated Temperatures:");
        for (int i = 0; i < matrixSize; i++) {
            System.out.printf("Node %d: %.4f°C\n", i + 1, temperatures[i]);
        }
    }
}