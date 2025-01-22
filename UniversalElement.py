import math
import numpy as np
from config import pc_mode
from GaussQuadrature import GaussQuadrature
from Surface import Surface

class UniversalElement:
    def __init__(self):
        self.gauss_quadrature = GaussQuadrature()
        self.surface = Surface(len(self.gauss_quadrature.get_pc_params()))
        self.npc = len(self.gauss_quadrature.get_pc_params())
        self.num_points = int(math.sqrt(pc_mode))
        self.ksi_eta_values = [param for param in self.gauss_quadrature.get_pc_params()]
        self.dNdKsi = np.zeros((self.npc, 4))
        self.dNdEta = np.zeros((self.npc, 4))
        self.surface_transformations = self.initialize_surface_transformations()
        self.calculate_derivatives()
        self.calculate_surface_values()

    def initialize_surface_transformations(self):
        return [
            lambda point: [point, -1.0],  # Dolna powierzchnia (eta = -1)
            lambda point: [1.0, point],  # Prawa powierzchnia (ksi = 1)
            lambda point: [point, 1.0],  # Górna powierzchnia (eta = 1)
            lambda point: [-1.0, point],  # Lewa powierzchnia (ksi = -1)
        ]

    def calculate_shape_functions(self, ksi, eta):
        N = np.zeros(4)
        N[0] = 0.25 * (1 - ksi) * (1 - eta)
        N[1] = 0.25 * (1 + ksi) * (1 - eta)
        N[2] = 0.25 * (1 + ksi) * (1 + eta)
        N[3] = 0.25 * (1 - ksi) * (1 + eta)
        return N

    def get_surface_shape_functions(self, surface_index, point):
        transformed_point = self.surface_transformations[surface_index](point)
        return self.calculate_shape_functions(transformed_point[0], transformed_point[1])

    def calculate_derivatives(self):
        for i in range(self.num_points):
            eta = self.ksi_eta_values[i][1]
            for j in range(self.num_points):
                ksi = self.ksi_eta_values[j][0]
                idx = i * self.num_points + j

                self.dNdKsi[idx][0] = -0.25 * (1 - eta)
                self.dNdKsi[idx][1] = 0.25 * (1 - eta)
                self.dNdKsi[idx][2] = 0.25 * (1 + eta)
                self.dNdKsi[idx][3] = -0.25 * (1 + eta)

                self.dNdEta[idx][0] = -0.25 * (1 - ksi)
                self.dNdEta[idx][1] = -0.25 * (1 + ksi)
                self.dNdEta[idx][2] = 0.25 * (1 + ksi)
                self.dNdEta[idx][3] = 0.25 * (1 - ksi)

    def calculate_surface_values(self):
        surface_N = self.surface.N
        for surface_index in range(4):
            for point_index in range(self.num_points):
                point = self.ksi_eta_values[point_index][0]
                N = self.get_surface_shape_functions(surface_index, point)
                surface_N[point_index][:] = N

    def print_results(self):
        print("------------------------------------------------------------")
        print("| pc | dN1/dKsi   | dN2/dKsi   | dN3/dKsi   | dN4/dKsi   |")
        print("------------------------------------------------------------")
        for p in range(self.npc):
            print(f"| {p + 1:2} ", end="")
            for value in self.dNdKsi[p]:
                print(f"| {value:8.5f} ", end="")
            print("|")
        print("------------------------------------------------------------")
        print("| pc | dN1/dEta   | dN2/dEta   | dN3/dEta   | dN4/dEta   |")
        print("------------------------------------------------------------")
        for p in range(self.npc):
            print(f"| {p + 1:2} ", end="")
            for value in self.dNdEta[p]:
                print(f"| {value:8.5f} ", end="")
            print("|")
        print("------------------------------------------------------------")
