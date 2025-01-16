package org.example;

public class FilePrinter {

    private FilePrinter() {}

     public static void printFromFile(GlobalData globalData){
         System.out.println("SimulationTime: " + globalData.getSimulationTime());
         System.out.println("SimulationStepTime: " + globalData.getSimulationStepTime());
         System.out.println("Conductivity: " + globalData.getConductivity());
         System.out.println("Alfa: " + globalData.getAlpha());
         System.out.println("Tot: " + globalData.getTot());
         System.out.println("InitialTemp: " + globalData.getInitialTemp());
         System.out.println("Density: " + globalData.getDensity());
         System.out.println("SpecificHeat: " + globalData.getSpecificHeat());
         System.out.println("Nodes number: " + globalData.getnN());
         System.out.println("Elements number: " + globalData.getnE());

         Grid grid = globalData.getGrid();
         System.out.println("\nNodes:");
         for (Node node : grid.getNodes()) {
             System.out.println(node);
         }

         System.out.println("\nElements:");
         for (Element element : grid.getElements()) {
             System.out.println(element);
         }
     }
}
