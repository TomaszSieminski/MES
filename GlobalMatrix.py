import numpy as np
from tabulate import tabulate

class GlobalMatrix:
    def __init__(self, size):
        self.matrix = np.zeros((size, size))

    def assemble(self, grid):
        for element in grid.elements:
            local_matrix = element.matrixH.H
            nodes = element.vertices

            for i in range(4):
                for j in range(4):
                    global_i = nodes[i] - 1
                    global_j = nodes[j] - 1
                    self.matrix[global_i][global_j] += local_matrix[i][j]

    def display(self):
        print("Macierz H Globalna")
        print(tabulate(self.matrix, tablefmt="plain", floatfmt=".4f"))
