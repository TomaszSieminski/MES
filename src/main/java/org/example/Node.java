package org.example;

public class Node {
    private final double x;
    private final double y;
    private boolean bc;
    private final int nodeID;

    public Node(double x, double y, int nodeID) {
        this.x = x;
        this.y = y;
        this.nodeID = nodeID;
        this.bc = false;
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }

    public boolean isBC() {
        return bc;
    }

    public void setBC(boolean bc) {
        this.bc = bc;
    }

    @Override
    public String toString() {
        return "Node " +  nodeID + " {" + "x=" + x + ", y=" + y + ", BC=" + bc +"}";
    }
}
