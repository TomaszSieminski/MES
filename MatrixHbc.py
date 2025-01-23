import numpy as np
from GaussQuadrature import gauss

class MatrixHbc:
    def __init__(self, element_nodes, alpha, tot):
        self.element_nodes = element_nodes
        self.alpha = alpha
        self.tot = tot
        self.gauss_points = gauss.pc_params
        self.gauss_weights = gauss.weights
        self.Hbc = np.zeros((4, 4))
        self.P_local = np.zeros(4)
        self.compute_hbc_and_p()

    def compute_hbc_and_p(self):
        edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

        for edge in edges:
            node1 = self.element_nodes[edge[0]]
            node2 = self.element_nodes[edge[1]]

            if node1.BC and node2.BC:
                edge_length = np.sqrt((node2.x - node1.x)**2 + (node2.y - node1.y)**2)

                for i, (ksi, eta) in enumerate(self.gauss_points):
                    weight = self.gauss_weights[i]
                    N = [0.5 * (1 - ksi), 0.5 * (1 + ksi)]

                    for a in range(2):
                        global_a = edge[a]
                        self.P_local[global_a] += self.alpha * self.tot * N[a] * edge_length * weight * 0.25

                        for b in range(2):
                            global_b = edge[b]
                            self.Hbc[global_a][global_b] += self.alpha * N[a] * N[b] * edge_length * weight * 0.25