package org.example;

public class SolveEquation {
    private final GlobalData globalData;
    private double[] vectorP;
    private double[] t0;
    private double[] t1;
    private double time;

    public SolveEquation(GlobalData globalData) {
        this.globalData = globalData;
        int numberOfNodes = globalData.getnN();
        this.t0 = new double[numberOfNodes];
        this.t1 = new double[numberOfNodes];
        this.time = 0.0;

        double initialTemp = globalData.getInitialTemp();
        for (int i = 0; i < numberOfNodes; i++) {
            t0[i] = initialTemp;
        }
    }

    public void calculateResults(int integrationPoints) {
        printHeader();

        Grid grid = globalData.getGrid();
        GlobalMatrixH globalMatrixH = new GlobalMatrixH(globalData);
        GlobalMatrixC globalMatrixC = new GlobalMatrixC(globalData);

        // Calculate matrices H, C, and vector P
        calculateGlobalMatrices(grid, globalMatrixH, globalMatrixC, integrationPoints);

        double simulationTime = globalData.getSimulationTime();
        double deltaT = globalData.getSimulationStepTime();
        int timeSteps = (int) (simulationTime / deltaT);

        printTimeStepResults();

        for (int step = 0; step < timeSteps; step++) {
            time += deltaT;

            // Create combined matrix [H] + [C]/dT
            double[][] leftSide = new double[globalData.getnN()][globalData.getnN()];
            for (int i = 0; i < globalData.getnN(); i++) {
                for (int j = 0; j < globalData.getnN(); j++) {
                    leftSide[i][j] = globalMatrixH.getGlobalMatrixH()[i][j] + globalMatrixC.getGlobalMatrixC()[i][j] / deltaT;
                }
            }

            // Calculate right side ([C]/dT)*{t0} + {P}
            double[] rightSide = new double[globalData.getnN()];
            for (int i = 0; i < globalData.getnN(); i++) {
                rightSide[i] = globalMatrixH.getGlobalP()[i];
                for (int j = 0; j < globalData.getnN(); j++) {
                    rightSide[i] += (globalMatrixC.getGlobalMatrixC()[i][j] * t0[j]) / deltaT;
                }
            }

            GaussSolver solver = new GaussSolver(globalData, leftSide, rightSide);
            t1 = solver.solve();

            //printTimeStepResults();
            printMinMaxTemperatures();

            System.arraycopy(t1, 0, t0, 0, t0.length);
        }
    }

    private void calculateGlobalMatrices(Grid grid, GlobalMatrixH globalMatrixH, GlobalMatrixC globalMatrixC, int integrationPoints) {
        ElementUni elementUni = new ElementUni(integrationPoints);

        for (Element element : grid.getElements()) {
            Jacobian jacobian = new Jacobian(integrationPoints, globalData, elementUni, element.getElementID());
            MatrixHbc matrixHbc = new MatrixHbc(globalData, element, integrationPoints);
            MatrixH matrixH = new MatrixH(integrationPoints, globalData, elementUni, jacobian);
            MatrixC matrixC = new MatrixC(integrationPoints, globalData, elementUni, jacobian);
            //matrixC.printMatrixC();

            matrixH.addHbc(matrixHbc);
            vectorP = matrixHbc.getP();

            globalMatrixH.calculateGlobalMatrixH(element, matrixH.getH());
            globalMatrixC.calculateGlobalMatrixC(element, matrixC.getC());
            globalMatrixH.aggregateP(element, vectorP);
        }
    }

    private void printHeader() {
        System.out.printf("SIMULATION DURATION: %.4fs\n", globalData.getSimulationTime());
        System.out.printf("SIMULATION TIME STEP : %.4fs\n\n", globalData.getSimulationStepTime());
    }

    private void printTimeStepResults() {
        System.out.printf("SIMULATION TIME: %.4f s\n", time);

        for (int i = 0; i < t1.length; i += 4) {
            StringBuilder line = new StringBuilder();
            for (int j = 0; j < 4 && (i + j) < t1.length; j++) {
                line.append(String.format("%.4f |   ", t1[i + j]));
            }
            System.out.println(line.toString()
                .trim());
        }

        // Min and max temperatures
        double minTemp = t1[0];
        double maxTemp = t1[0];
        for (int i = 1; i < t1.length; i++) {
            minTemp = Math.min(minTemp, t1[i]);
            maxTemp = Math.max(maxTemp, t1[i]);
        }

        System.out.printf("Max temperature this step: %.14f\n", maxTemp);
        System.out.printf("Min temperature this step: %.14f\n\n", minTemp);
    }

    private void printMinMaxTemperatures() {
        // Min and max temperatures
        double minTemp = t1[0];
        double maxTemp = t1[0];
        for (int i = 1; i < t1.length; i++) {
            minTemp = Math.min(minTemp, t1[i]);
            maxTemp = Math.max(maxTemp, t1[i]);
        }

        System.out.printf("%.14f\t%.14f\n", minTemp, maxTemp);
    }
}