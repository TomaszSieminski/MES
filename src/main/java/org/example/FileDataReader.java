package org.example;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class FileDataReader {

    public static GlobalData readFile(String filePath) {
        GlobalData globalData = null;
        Grid grid;

        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            boolean readingNodes = false;
            boolean readingElements = false;
            boolean readingBC = false;
            Node[] nodes = null;
            Element[] elements = null;
            int nodeIndex = 0;
            int elementIndex = 0;

            while ((line = br.readLine()) != null) {
                String[] tokens = line.trim().split("[,\\s]+");

                if (line.startsWith("SimulationTime")) {
                    globalData = new GlobalData(
                        Double.parseDouble(tokens[1]), 0, 0, 0, 0, 0, 0, 0, 0, 0
                    );
                } else if (line.startsWith("SimulationStepTime")) {
                    globalData.setSimulationStepTime(Double.parseDouble(tokens[1]));
                } else if (line.startsWith("Conductivity")) {
                    globalData.setConductivity(Double.parseDouble(tokens[1]));
                } else if (line.startsWith("Alfa")) {
                    globalData.setAlpha(Double.parseDouble(tokens[1]));
                } else if (line.startsWith("Tot")) {
                    globalData.setTot(Double.parseDouble(tokens[1]));
                } else if (line.startsWith("InitialTemp")) {
                    globalData.setInitialTemp(Double.parseDouble(tokens[1]));
                } else if (line.startsWith("Density")) {
                    globalData.setDensity(Double.parseDouble(tokens[1]));
                } else if (line.startsWith("SpecificHeat")) {
                    globalData.setSpecificHeat(Double.parseDouble(tokens[1]));
                } else if (line.startsWith("Nodes number")) {
                    int nN = Integer.parseInt(tokens[2]);
                    globalData.setnN(nN);
                    nodes = new Node[nN];
                } else if (line.startsWith("Elements number")) {
                    int nE = Integer.parseInt(tokens[2]);
                    globalData.setnE(nE);
                    elements = new Element[nE];
                } else if (line.startsWith("*Node")) {
                    readingNodes = true;
                } else if (line.startsWith("*Element")) {
                    readingNodes = false;
                    readingElements = true;
                } else if (line.startsWith("*BC")) {
                    readingElements = false;
                    readingBC = true;
                }

                if (readingNodes && !line.startsWith("*Node")) {
                    try {
                        int nodeID = Integer.parseInt(tokens[0]);
                        double x = Double.parseDouble(tokens[1]);
                        double y = Double.parseDouble(tokens[2]);
                        nodes[nodeIndex++] = new Node(x, y, nodeID);
                    } catch (Exception e) {
                        throw new IllegalArgumentException("Error parsing node data: " + line, e);
                    }
                }

                if (readingElements && !line.startsWith("*Element")) {
                    try {
                        int elementID = Integer.parseInt(tokens[0]);
                        int[] ids = new int[4];
                        for (int i = 0; i < 4; i++) {
                            ids[i] = Integer.parseInt(tokens[i + 1]);
                        }
                        elements[elementIndex++] = new Element(ids, elementID);
                    } catch (Exception e) {
                        throw new IllegalArgumentException("Error parsing element data: " + line, e);
                    }
                }

                if (readingBC && !line.startsWith("*BC")) {
                    for (String token : tokens) {
                        try {
                            int nodeId = Integer.parseInt(token.trim());
                            if (nodeId > 0 && nodeId <= nodes.length) {
                                nodes[nodeId - 1].setBC(true);
                            } else {
                                throw new IllegalArgumentException("Invalid BC node ID: " + nodeId);
                            }
                        } catch (NumberFormatException e) {
                            throw new IllegalArgumentException("Error parsing BC data: " + line, e);
                        }
                    }
                }
            }

            if (globalData != null) {
                grid = new Grid(globalData.getnN(), globalData.getnE());
                grid.setNodes(nodes);
                grid.setElements(elements);
                globalData.setGrid(grid);
            } else {
                throw new IllegalStateException("GlobalData was not initialized.");
            }

        } catch (IOException e) {
            System.err.println("File could not be read: " + e.getMessage());
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("Error processing file: " + e.getMessage());
            e.printStackTrace();
        }

        return globalData;
    }
}
