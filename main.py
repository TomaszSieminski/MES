from Simulation import Simulation
from GlobalMatrix import GlobalMatrix
import config

def main():
    simulation = Simulation()
    simulation.readData(config.file_path)
    #simulation.displayData()

    simulation.grid.calc_jacobian_and_h_for_elem()
    #simulation.grid.display_jacobian_and_h_matrices()

    simulation.grid.calc_hbc_for_elem(simulation.globalData.alpha, simulation.globalData.ambientTemp)
    #simulation.grid.display_hbc_matrices()

    global_matrix = GlobalMatrix(simulation.globalData.nN)
    global_matrix.assemble_h(simulation.grid)
    #global_matrix.display_h()
    global_matrix.assemble_hbc(simulation.grid)
    #global_matrix.display_hbc()
    global_matrix.assemble_p(simulation.grid)
    #global_matrix.display_p()

    simulation.grid.calc_c_for_elem(simulation.globalData.density, simulation.globalData.specificHeat)
    #simulation.grid.display_c_matrices()

    global_matrix.assemble_c(simulation.grid)
    #global_matrix.display_c()

if __name__ == "__main__":
    main()