from Grid import Grid
from Grid import Node
from Grid import Element

class GlobalData:
    def __init__(self, variables):
        self.simulationTime = variables[find_value(variables, 'SimulationTime')][1]
        self.simulationStepTime = variables[find_value(variables, 'SimulationStepTime')][1]
        self.conductivity = variables[find_value(variables, 'Conductivity')][1]
        self.alpha = variables[find_value(variables, 'Alfa')][1]
        self.ambientTemp = variables[find_value(variables, 'Tot')][1]
        self.initialTemp = variables[find_value(variables, 'InitialTemp')][1]
        self.density = variables[find_value(variables, 'Density')][1]
        self.specificHeat = variables[find_value(variables, 'SpecificHeat')][1]
        self.nN = variables[find_value(variables, 'Nodes number')][1]
        self.nE = variables[find_value(variables, 'Elements number')][1]

    def __str__(self):
        return (f"""
        SimulationTime = {self.simulationTime}, 
        SimulationStepTime = {self.simulationStepTime}, 
        Conductivity = {self.conductivity}, 
        Alfa = {self.alpha}, 
        Tot = {self.ambientTemp}, 
        InitialTemp = {self.initialTemp}, 
        Density = {self.density}, 
        SpecificHeat = {self.specificHeat}, 
        Nodes number = {self.nN}, 
        Elements number = {self.nE}
        """)

class Simulation:
    def __init__(self):
        self.globalData = None
        self.grid = None

    def readData(self, path):
        with open(path, 'r') as file:
            variables = []
            nodes = []
            elements = []

            lines = file.readlines()

            for x in range(10):
                varName = " ".join(lines[x].split()[:-1])
                varValue = int(lines[x].split()[-1])

                variables.append([varName, varValue])

            self.globalData = GlobalData(variables)

            for i in range(11, 11 + self.globalData.nN):
                parts = lines[i].split(',')
                nodes.append(Node(int(parts[0].strip()), float(parts[1].strip()), float(parts[2].strip())))

            for i in range(12 + self.globalData.nN, 12 + self.globalData.nN + self.globalData.nE):
                parts = lines[i].split(',')
                elemtId = int(parts[0])
                vert = []
                for x in range(1, len(parts)):
                    vert.append(int(parts[x].strip()))
                elem = Element(elemtId, vert)
                elements.append(elem)

            for i, line in enumerate(lines):
                if line.strip() == "*BC":
                    bc_line = lines[i + 1].strip()
                    boundary_conditions = [int(x) for x in bc_line.split(',')]
                    break

            self.grid = Grid(self.globalData.nN, self.globalData.nE, elements, nodes, self.globalData)

            for node in self.grid.nodes:
                if node.id in boundary_conditions:
                    node.BC = 1
                else:
                    node.BC = 0


    def displayData(self):
            print(self.globalData)
            print("Nodes:")
            for node in self.grid.nodes:
                print(node)
            print("Elements:")
            for element in self.grid.elements:
                print(element)

def find_value(array, value):
    for i in range(len(array)):
        if array[i][0] == value:
            return i