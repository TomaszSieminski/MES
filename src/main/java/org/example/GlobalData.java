package org.example;

public class GlobalData {
    private double simulationTime;
    private double simulationStepTime;
    private double conductivity;
    private double alpha;
    private double tot;
    private double initialTemp;
    private double density;
    private double specificHeat;
    private int nN;
    private int nE;
    private Grid grid;

    public GlobalData(double simulationTime, double simulationStepTime, double conductivity, double alpha,
                      double tot, double initialTemp, double density, double specificHeat, int nN, int nE) {
        this.simulationTime = simulationTime;
        this.simulationStepTime = simulationStepTime;
        this.conductivity = conductivity;
        this.alpha = alpha;
        this.tot = tot;
        this.initialTemp = initialTemp;
        this.density = density;
        this.specificHeat = specificHeat;
        this.nN = nN;
        this.nE = nE;
        this.grid = new Grid(nN, nE);
    }

    public double getSimulationTime() {
        return simulationTime;
    }

    public void setSimulationTime(double simulationTime) {
        this.simulationTime = simulationTime;
    }

    public double getSimulationStepTime() {
        return simulationStepTime;
    }

    public void setSimulationStepTime(double simulationStepTime) {
        this.simulationStepTime = simulationStepTime;
    }

    public double getConductivity() {
        return conductivity;
    }

    public void setConductivity(double conductivity) {
        this.conductivity = conductivity;
    }

    public double getAlpha() {
        return alpha;
    }

    public void setAlpha(double alpha) {
        this.alpha = alpha;
    }

    public double getTot() {
        return tot;
    }

    public void setTot(double tot) {
        this.tot = tot;
    }

    public double getInitialTemp() {
        return initialTemp;
    }

    public void setInitialTemp(double initialTemp) {
        this.initialTemp = initialTemp;
    }

    public double getDensity() {
        return density;
    }

    public void setDensity(double density) {
        this.density = density;
    }

    public double getSpecificHeat() {
        return specificHeat;
    }

    public void setSpecificHeat(double specificHeat) {
        this.specificHeat = specificHeat;
    }

    public int getnN() {
        return nN;
    }

    public void setnN(int nN) {
        this.nN = nN;
    }

    public int getnE() {
        return nE;
    }

    public void setnE(int nE) {
        this.nE = nE;
    }

    public Grid getGrid() {
        return grid;
    }

    public void setGrid(Grid grid) {
        this.grid = grid;
    }

    @Override
    public String toString() {
        return "GlobalData{" +
                "simulationTime=" + simulationTime +
                ", simulationStepTime=" + simulationStepTime +
                ", conductivity=" + conductivity +
                ", alpha=" + alpha +
                ", tot=" + tot +
                ", initialTemp=" + initialTemp +
                ", density=" + density +
                ", specificHeat=" + specificHeat +
                ", nN=" + nN +
                ", nE=" + nE +
                '}';
    }
}