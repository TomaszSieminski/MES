import config
from GlobalData import GlobalData
from Grid import Grid
from Grid import Node
from Grid import Element
from GlobalMatrix import GlobalMatrix
from SolveEquation import SolveEquation
from GridPlotter import GridPlotter
import numpy as np
import csv

class Simulation:
    def __init__(self):
        self.time_steps = []
        self.min_temperatures = []
        self.max_temperatures = []
        self.globalData = None
        self.grid = None

    def run_simulation(self):
        self.readData(config.file_path)

        if config.gridplotter:
            plotter = GridPlotter(self.grid)
            plotter.plot_grid()

        simulation_time = self.globalData.simulationTime
        time_step = self.globalData.simulationStepTime

        num_nodes = len(self.grid.nodes)
        t_prev = [self.globalData.initialTemp] * num_nodes
        t_curr = [0.0] * num_nodes

        self.grid.calc_jacobian_and_h_for_elem()
        self.grid.calc_hbc_for_elem(self.globalData.alpha, self.globalData.ambientTemp)
        global_matrix = GlobalMatrix(self.grid.globalData.nN)
        global_matrix.assemble_h(self.grid)
        global_matrix.assemble_hbc(self.grid)
        global_matrix.assemble_p(self.grid)
        self.grid.calc_c_for_elem(self.globalData.density, self.globalData.specificHeat)
        global_matrix.assemble_c(self.grid)

        if config.VERBOSE:
            self.displayData()
            self.grid.display_jacobian()
            self.grid.display_h_matrices()
            global_matrix.display_h()
            self.grid.display_hbc_matrices()
            global_matrix.display_hbc()
            global_matrix.display_p()
            self.grid.display_c_matrices()
            global_matrix.display_c()

        print("\n\tSTART OF SIMULATION\n")

        for current_time in np.arange(0.0, simulation_time, time_step):
            print(f"SIMULATION TIME: {current_time + time_step:.2f} s")

            # H = H + C / dt
            H_total = np.array(global_matrix.Hbc) + np.array(global_matrix.C) / time_step

            # P = P + (C / dt) * T_prev
            P_total = np.array(global_matrix.P) + (np.array(global_matrix.C) / time_step).dot(t_prev)

            # H_total * T_curr = P_total
            t_curr = SolveEquation.solve(H_total, P_total)

            if config.all_temperatures:
                for i, temp in enumerate(t_curr):
                    print(f"T[{i}] = {temp:.4f}", end="\t")
                    if (i + 1) % 4 == 0:
                        print()
                print()

            max_temp = max(t_curr)
            min_temp = min(t_curr)
            self.max_temperatures.append(max_temp)
            self.min_temperatures.append(min_temp)
            self.time_steps.append(current_time + time_step)

            print(f"Max temperature this step: {max_temp:.10f}")
            print(f"Min temperature this step: {min_temp:.10f}\n")

            t_prev = t_curr.tolist()

        print("\n\tEND OF SIMULATION\n")

        print("\nMax Temperatures during simulation:")
        print(" ".join(f"{temp:.10f}" for temp in self.max_temperatures))

        print("\nMin Temperatures during simulation:")
        print(" ".join(f"{temp:.10f}" for temp in self.min_temperatures))

        self.save_results_to_csv("simulation_results.csv")

    def save_results_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=';')
            header = ["Time", "Min Temperature", "Max Temperature"]
            csv_writer.writerow(header)

            for i, time in enumerate(self.time_steps):
                row = [time, self.min_temperatures[i], self.max_temperatures[i]]
                csv_writer.writerow(row)
        print(f"Results saved to '{filename}'")

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