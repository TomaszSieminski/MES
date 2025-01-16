package org.example;

public class Element {
    private final int[] elements = new int[4];
    private final int elementID;

    public Element(int[] ID, int elementID) {
        if (ID.length == 4) {
            System.arraycopy(ID, 0, this.elements, 0, ID.length);
            this.elementID = elementID;
        } else {
            throw new IllegalArgumentException("Elements array must have exactly 4 elements.");
        }
    }

    public int[] getElements() {
        return elements;
    }

    public int getElementID() {
        return elementID;
    }

    @Override
    public String toString() {
        return "Element " +  elementID + " {" + "ID=" + java.util.Arrays.toString(elements) + "}";
    }
}
