from Simulation import Simulation
from GlobalMatrix import GlobalMatrix
import config

def main():
    simulation = Simulation()
    simulation.readData(config.file_path)
    #simulation.displayData()
    simulation.grid.calc_jacobian_and_H_for_elem()

    global_matrix = GlobalMatrix(simulation.globalData.nN)
    global_matrix.assemble(simulation.grid)
    #global_matrix.display()

    simulation.grid.calc_hbc_for_elem(simulation.globalData.alpha, simulation.globalData.ambientTemp)
    simulation.grid.display_hbc_matrices()

if __name__ == "__main__":
    main()