import numpy as np
from GaussQuadrature import gauss

class MatrixC:
    def __init__(self, element_nodes, detj, density, specific_heat):
        self.C_local = np.zeros((4, 4))
        self.detJ = detj
        self.density = density
        self.specific_heat = specific_heat
        self.element_nodes = element_nodes
        self.gauss_points = gauss.pc_params
        self.weights = gauss.weights


        self.calculate_c_matrix()

    def calculate_c_matrix(self):
        for i, (ksi, eta) in enumerate(self.gauss_points):
            shape_functions = self.calculate_shape_functions(ksi, eta)

            for a in range(4):
                for b in range(4):
                    self.C_local[a][b] += (
                        self.density * self.specific_heat *
                        shape_functions[a] * shape_functions[b] *
                        self.detJ[i] * self.weights[i]
                    )

    def calculate_shape_functions(self, ksi, eta):
        return [
            0.25 * (1 - ksi) * (1 - eta),
            0.25 * (1 + ksi) * (1 - eta),
            0.25 * (1 + ksi) * (1 + eta),
            0.25 * (1 - ksi) * (1 + eta)
        ]
