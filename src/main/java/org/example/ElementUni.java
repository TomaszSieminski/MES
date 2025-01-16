package org.example;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

public class ElementUni {
    private final double[] ksiEtaValues;
    private final double[][] dNdKsi;
    private final double[][] dNdEta;
    private final int npc;
    private final int numPoints;
    private final List<Function<Double, double[]>> surfaceTransformations;
    private final Surface surface;

    public ElementUni(int integrationPoints) {
        this.npc = integrationPoints * integrationPoints;
        this.numPoints = integrationPoints;
        GaussQuadratureData gaussQuadratureData = new GaussQuadratureData(integrationPoints);
        this.ksiEtaValues = gaussQuadratureData.getNodes();
        dNdKsi = new double[npc][4];
        dNdEta = new double[npc][4];
        surface = new Surface(integrationPoints);
        surfaceTransformations = initializeSurfaceTransformations();
        calculateDerivatives();
        calculateSurfaceValues();
    }

    private List<Function<Double, double[]>> initializeSurfaceTransformations() {
        List<Function<Double, double[]>> transformations = new ArrayList<>();
        // Bottom surface (eta = -1)
        transformations.add(point -> new double[]{point, -1.0});
        // Right surface (ksi = 1)
        transformations.add(point -> new double[]{1.0, point});
        // Top surface (eta = 1)
        transformations.add(point -> new double[]{point, 1.0});
        // Left surface (ksi = -1)
        transformations.add(point -> new double[]{-1.0, point});
        return transformations;
    }

    public double[] calculateShapeFunctions(double ksi, double eta) {
        double[] N = new double[4];
        N[0] = 0.25 * (1 - ksi) * (1 - eta);
        N[1] = 0.25 * (1 + ksi) * (1 - eta);
        N[2] = 0.25 * (1 + ksi) * (1 + eta);
        N[3] = 0.25 * (1 - ksi) * (1 + eta);
        return N;
    }

    public double[] getSurfaceShapeFunctions(int surfaceIndex, double point) {
        double[] transformedPoint = surfaceTransformations.get(surfaceIndex).apply(point);
        return calculateShapeFunctions(transformedPoint[0], transformedPoint[1]);
    }

    private void calculateDerivatives() {
        for (int i = 0; i < numPoints; i++) {
            double eta = ksiEtaValues[i];
            for (int j = 0; j < numPoints; j++) {
                double ksi = ksiEtaValues[j];
                int idx = i * numPoints + j;

                dNdKsi[idx][0] = -0.25 * (1 - eta);
                dNdKsi[idx][1] = 0.25 * (1 - eta);
                dNdKsi[idx][2] = 0.25 * (1 + eta);
                dNdKsi[idx][3] = -0.25 * (1 + eta);

                dNdEta[idx][0] = -0.25 * (1 - ksi);
                dNdEta[idx][1] = -0.25 * (1 + ksi);
                dNdEta[idx][2] = 0.25 * (1 + ksi);
                dNdEta[idx][3] = 0.25 * (1 - ksi);
            }
        }
    }

    private void calculateSurfaceValues() {
        double[][] surfaceN = surface.getN();
        for (int surfaceIndex = 0; surfaceIndex < 4; surfaceIndex++) {
            for (int pointIndex = 0; pointIndex < numPoints; pointIndex++) {
                double point = ksiEtaValues[pointIndex];
                double[] N = getSurfaceShapeFunctions(surfaceIndex, point);
                System.arraycopy(N, 0, surfaceN[pointIndex], 0, 4);
            }
        }
    }


    public double[] getKsiEtaValues() {
        return ksiEtaValues;
    }

    public double[][] getdNdKsi() {
        return dNdKsi;
    }

    public double[][] getdNdEta() {
        return dNdEta;
    }

    public Surface getSurface() {
        return surface;
    }

    public int getNumPoints() {
        return numPoints;
    }

    public void printResults() {
        System.out.println("------------------------------------------------------------");
        System.out.println("| pc | dN1/dKsi   | dN2/dKsi   | dN3/dKsi   | dN4/dKsi   |");
        System.out.println("------------------------------------------------------------");

        for (int p = 0; p < npc; p++) {
            System.out.print("| " + (p + 1) + "  ");
            for (int j = 0; j < dNdKsi[0].length; j++) {
                System.out.printf("| %-8.5f ", dNdKsi[p][j]);
            }
            System.out.println("|");
        }

        System.out.println("------------------------------------------------------------");
        System.out.println("| pc | dN1/dEta   | dN2/dEta   | dN3/dEta   | dN4/dEta   |");
        System.out.println("------------------------------------------------------------");

        for (int p = 0; p < npc; p++) {
            System.out.print("| " + (p + 1) + "  ");
            for (int j = 0; j < dNdEta[0].length; j++) {
                System.out.printf("| %-8.5f ", dNdEta[p][j]);
            }
            System.out.println("|");
        }
        System.out.println("------------------------------------------------------------");
    }
}