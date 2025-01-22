import numpy as np
import math
from UniversalElement import UniversalElement
from GaussQuadrature import GaussQuadrature
from config import pc_mode
from tabulate import tabulate

class MatrixHbc:
    def __init__(self, global_data, grid, element):
        self.global_data = global_data
        self.grid = grid
        self.element = element
        self.num_points = int(math.sqrt(pc_mode))
        self.Hbc = np.zeros((4, 4))
        self.P = np.zeros(4)
        self.element_uni = UniversalElement()

        self.calculate_matrix_Hbc_and_vector_P()

    def get_Hbc(self):
        return self.Hbc

    def get_P(self):
        return self.P

    def calculate_matrix_Hbc_and_vector_P(self):
        weights = GaussQuadrature().get_weights()
        alpha = self.global_data.alpha

        for edge in range(4):  # Iteracja po krawędziach
            nodes = self.get_edge_nodes(edge)

            if nodes[0].BC == 0 and nodes[1].BC == 0:
                continue

            det_j = self.calculate_edge_length(nodes[0], nodes[1]) / 2.0

            for i in range(self.num_points):
                ksi, eta = self.element_uni.ksi_eta_values[i]
                N = self.element_uni.get_surface_shape_functions(edge, ksi)

                for j in range(4):
                    for k in range(4):
                        self.Hbc[j][k] += alpha * N[j] * N[k] * weights[i] * det_j

                    tot = self.global_data.ambientTemp
                    self.P[j] += alpha * N[j] * weights[i] * det_j * tot

    def get_edge_nodes(self, edge):
        node_ids = self.element.vertices
        nodes = [None, None]

        if edge == 0:  # bottom
            nodes[0] = self.grid.get_node_by_id(node_ids[0])
            nodes[1] = self.grid.get_node_by_id(node_ids[1])
        elif edge == 1:  # right
            nodes[0] = self.grid.get_node_by_id(node_ids[1])
            nodes[1] = self.grid.get_node_by_id(node_ids[2])
        elif edge == 2:  # top
            nodes[0] = self.grid.get_node_by_id(node_ids[2])
            nodes[1] = self.grid.get_node_by_id(node_ids[3])
        elif edge == 3:  # left
            nodes[0] = self.grid.get_node_by_id(node_ids[3])
            nodes[1] = self.grid.get_node_by_id(node_ids[0])

        return nodes

    @staticmethod
    def calculate_edge_length(n1, n2):
        dx = n2.x - n1.x
        dy = n2.y - n1.y
        return np.sqrt(dx ** 2 + dy ** 2)

    def print_vector_P(self):
        print("Vector P:")
        print(tabulate([self.P], tablefmt="plain", floatfmt=".5f"))

    def print_Hbc(self):
        print("Macierz Hbc:")
        print(tabulate(self.Hbc, tablefmt="plain", floatfmt=".5f"))
