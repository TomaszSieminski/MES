package org.example;

public class MatrixHbc {
    private final double[][] Hbc;
    private final double[] P;
    private final GlobalData globalData;
    private final Element element;
    private final Grid grid;
    private final ElementUni elementUni;
    private final int numPoints;

    public MatrixHbc(GlobalData globalData, Element element, int numPoints) {
        this.globalData = globalData;
        this.element = element;
        this.grid = globalData.getGrid();
        this.numPoints = numPoints;
        this.Hbc = new double[4][4];
        this.P = new double[4];
        this.elementUni = new ElementUni(numPoints);

        calculateMatrixHbcAndVectorP();
    }

    public double[][] getHbc() {
        return Hbc;
    }

    public double[] getP() {
        return P;
    }

    private void calculateMatrixHbcAndVectorP() {
        double[] weights = new GaussQuadratureData(numPoints).getWeights();
        double alpha = globalData.getAlpha();

        for (int edge = 0; edge < 4; edge++) {
            Node[] nodes = getEdgeNodes(edge);

            if (!nodes[0].isBC() || !nodes[1].isBC()) {
                continue;
            }

            double detJ = calculateEdgeLength(nodes[0], nodes[1]) / 2.0;

            for (int i = 0; i < numPoints; i++) {
                double[] N = elementUni.getSurfaceShapeFunctions(edge, elementUni.getKsiEtaValues()[i]);

                for (int j = 0; j < 4; j++) {
                    for (int k = 0; k < 4; k++) {
                        Hbc[j][k] += alpha * N[j] * N[k] * weights[i] * detJ;
                    }

                    double tot = globalData.getTot();
                    P[j] += alpha * N[j] * weights[i] * detJ * tot;
                }
            }
        }
    }

    private Node[] getEdgeNodes(int edge) {
        int[] nodeIds = element.getElements();
        Node[] nodes = new Node[2];

        switch (edge) {
            case 0: // bottom
                nodes[0] = grid.getNodes()[nodeIds[0] - 1];
                nodes[1] = grid.getNodes()[nodeIds[1] - 1];
                break;
            case 1: // right
                nodes[0] = grid.getNodes()[nodeIds[1] - 1];
                nodes[1] = grid.getNodes()[nodeIds[2] - 1];
                break;
            case 2: // top
                nodes[0] = grid.getNodes()[nodeIds[2] - 1];
                nodes[1] = grid.getNodes()[nodeIds[3] - 1];
                break;
            case 3: // left
                nodes[0] = grid.getNodes()[nodeIds[3] - 1];
                nodes[1] = grid.getNodes()[nodeIds[0] - 1];
                break;
        }
        return nodes;
    }

    private double calculateEdgeLength(Node n1, Node n2) {
        double dx = n2.getX() - n1.getX();
        double dy = n2.getY() - n1.getY();
        return Math.sqrt(dx * dx + dy * dy);
    }

    public void printVectorP() {
        System.out.println("Vector P:");
        for (double value : P) {
            System.out.printf("| %8.5f ", value);
        }
        System.out.println("|");
    }
}