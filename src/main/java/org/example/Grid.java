package org.example;

public class Grid {
    private int nN;
    private int nE;
    private Node[] nodes;
    private Element[] elements;

    public Grid(int nN, int nE) {
        this.nN = nN;
        this.nE = nE;
        this.nodes = new Node[nN];
        this.elements = new Element[nE];
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

    public Node[] getNodes() {
        return nodes;
    }

    public void setNodes(Node[] nodes) {
        this.nodes = nodes;
    }

    public Element[] getElements() {
        return elements;
    }

    public void setElements(Element[] elements) {
        this.elements = elements;
    }

    @Override
    public String toString() {
        return "Grid{" + "nN=" + nN + ", nE=" + nE + '}';
    }
}
