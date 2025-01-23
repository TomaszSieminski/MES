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

def find_value(array, value):
    for i in range(len(array)):
        if array[i][0] == value:
            return i