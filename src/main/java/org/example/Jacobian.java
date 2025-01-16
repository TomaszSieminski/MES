package org.example;

public class Jacobian {
    private final double[][][] J;
    private final double[][][] J1;
    private final double[] detJ;
    private final int npc;
    private final double[][] dNdKsi;
    private final double[][] dNdEta;
    private final GlobalData globalData;
    private final int currentElementID;

    public Jacobian(int integrationPoints, GlobalData globalData, ElementUni elementUni, int elementID) {
        this.npc = integrationPoints * integrationPoints;
        currentElementID = elementID;
        J = new double[npc][2][2];
        J1 = new double[npc][2][2];
        detJ = new double[npc];
        dNdKsi = elementUni.getdNdKsi();
        dNdEta = elementUni.getdNdEta();
        this.globalData = globalData;
        calculateJacobians();
    }

    private void calculateJacobians() {
        Node[] nodes = globalData.getGrid().getNodes();
        Element[] elements = globalData.getGrid().getElements();

        if (currentElementID <= 0 || currentElementID > elements.length) {
            throw new IllegalArgumentException("Invalid element ID: " + currentElementID);
        }

        int[] currentElement = elements[currentElementID - 1].getElements();

        for (int p = 0; p < npc; p++) {
            J[p] = new double[][]{{0.0, 0.0}, {0.0, 0.0}};

            for (int i = 0; i < currentElement.length; i++) {
                // Sprawdzamy czy węzeł istnieje
                int currentNodeID = currentElement[i];
                if (currentNodeID <= 0 || currentNodeID > nodes.length) {
                    throw new IllegalArgumentException("Invalid node ID: " + currentNodeID);
                }

                double x = nodes[currentNodeID - 1].getX();
                double y = nodes[currentNodeID - 1].getY();

                J[p][0][0] += dNdKsi[p][i] * x;  // dXdKsi
                J[p][0][1] += dNdKsi[p][i] * y;  // dYdKsi
                J[p][1][0] += dNdEta[p][i] * x;  // dXdEta
                J[p][1][1] += dNdEta[p][i] * y;  // dYdEta
            }

            detJ[p] = calculateDetJ(J[p]);
            J1[p] = invertJacobian(J[p], detJ[p]);
        }
    }

    // Pozostałe metody pozostają bez zmian...
    public double[][] getJ(int pointIndex) {
        if (pointIndex < 0 || pointIndex >= npc) {
            throw new IllegalArgumentException("Invalid point index: " + pointIndex);
        }
        return J[pointIndex];
    }

    public double[][][] getJ1() {
        return J1;
    }

    public double[] getDetJ() {
        return detJ;
    }

    private double calculateDetJ(double[][] jacobianMatrix) {
        return jacobianMatrix[0][0] * jacobianMatrix[1][1] - jacobianMatrix[0][1] * jacobianMatrix[1][0];
    }

    private double[][] invertJacobian(double[][] jacobianMatrix, double detJ) {
        if (Math.abs(detJ) < 1e-10) {
            throw new IllegalStateException("Jacobian determinant is too close to zero: " + detJ);
        }

        double[][] inverse = new double[2][2];
        inverse[0][0] = jacobianMatrix[1][1] / detJ;
        inverse[0][1] = -jacobianMatrix[0][1] / detJ;
        inverse[1][0] = -jacobianMatrix[1][0] / detJ;
        inverse[1][1] = jacobianMatrix[0][0] / detJ;
        return inverse;
    }
}
