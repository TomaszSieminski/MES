from Simulation import Simulation
from GlobalMatrix import GlobalMatrix
import config

def main():
    simulation = Simulation()
    simulation.readData(config.file_path)
    #simulation.displayData()
    simulation.grid.calc_jacobian_for_elem()

    global_matrix = GlobalMatrix(simulation.globalData.nN)
    global_matrix.assemble(simulation.grid)
    #global_matrix.display()

    simulation.grid.calc_Hbc_for_elem()

if __name__ == "__main__":
    main()