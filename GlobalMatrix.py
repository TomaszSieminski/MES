import numpy as np
from tabulate import tabulate

class GlobalMatrix:
    def __init__(self, size):
        self.H = np.zeros((size, size))
        self.Hbc = np.zeros((size, size))
        self.P = np.zeros(size)
        self.C = np.zeros((size, size))

    def assemble_h(self, grid):
        for element in grid.elements:
            local_matrixH = element.H
            nodes = element.vertices

            for i in range(4):
                for j in range(4):
                    global_i = nodes[i] - 1
                    global_j = nodes[j] - 1
                    self.H[global_i][global_j] += local_matrixH[i][j]


    def assemble_hbc(self, grid):
        for element in grid.elements:
            self.Hbc = self.H
            local_matrixHbc = element.Hbc
            nodes = element.vertices

            for i in range(4):
                for j in range(4):
                    global_i = nodes[i] - 1
                    global_j = nodes[j] - 1
                    self.Hbc[global_i][global_j] += local_matrixHbc[i][j]
        return self.Hbc

    def assemble_p(self, grid):
        for element in grid.elements:
            local_P = element.P
            nodes = element.vertices

            for i in range(4):
                global_i = nodes[i] - 1
                self.P[global_i] += local_P[i]
        return self.P

    def assemble_c(self, grid):
        for element in grid.elements:
            local_C = element.C
            nodes = element.vertices

            for i in range(4):
                for j in range(4):
                    global_i = nodes[i] - 1
                    global_j = nodes[j] - 1
                    self.C[global_i, global_j] += local_C[i][j]
        return self.C

    def display_h(self):
        print("Global H Matrix:")
        print(tabulate(self.H, tablefmt="plain", floatfmt=".4f"))

    def display_hbc(self):
        print("Global HBC Matrix:")
        print(tabulate(self.Hbc, tablefmt="plain", floatfmt=".4f"))

    def display_p(self):
        print("Global P Vector:")
        print(" ".join(f"{value:.4f}" for value in self.P))

    def display_c(self):
        print("Global C Matrix:")
        print(tabulate(self.C, tablefmt="plain", floatfmt=".4f"))
