from Jacobian import Jacobian
from MatrixH import MatrixH
from MatrixHbc import MatrixHbc
from MatrixC import MatrixC
from tabulate import tabulate

class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.BC = 0

    def __str__(self):
        return str(self.id) + ", " + str(self.x) + ", " + str(self.y) + ", " + str(self.BC)


class Element:
    def __init__(self, id, vertices):
        self.id = id
        self.vertices = vertices
        self.jacobian = None
        self.H = []
        self.Hbc = []
        self.P = []
        self.C = []

    def calculate_jacobian_and_h(self, nodes, conductivity):
        self.jacobian = Jacobian(nodes)
        matrix_h = MatrixH(self.jacobian, conductivity)
        self.H = matrix_h.H

    def calculate_hbc(self, nodes, alpha, tot):
        element_nodes = [nodes[node_id - 1] for node_id in self.vertices]
        matrix_hbc = MatrixHbc(element_nodes, alpha, tot)
        self.Hbc = matrix_hbc.Hbc
        self.P = matrix_hbc.P_local

    def calculate_c(self, nodes, density, specific_heat):
        element_nodes = [nodes[node_id - 1] for node_id in self.vertices]
        matrix_c = MatrixC(element_nodes, self.jacobian.detJ, density, specific_heat)
        self.C = matrix_c.C_local

    def display_jacobian_and_h(self):
        print("Element", self.id)
        self.jacobian.__str__()

    def display_hbc_matrix(self):
        print(f"Element {self.id}:")
        print("Hbc Matrix:")
        print(tabulate(self.Hbc, tablefmt="plain", floatfmt=".4f"))
        print("P Vector:")
        print("  ", "  ".join(f"{value:.4f}" for value in self.P))
        print()

    def display_c_matrix(self):
        print(f"Element {self.id}:")
        print("C Matrix:")
        print(tabulate(self.C, tablefmt="plain", floatfmt=".4f"))


    def __str__(self):
        return str(self.id) + " (" + str(self.vertices) + ")"


class Grid:
    def __init__(self, nN, nE, elements, nodes, globalData):
        self.nN = nN
        self.nE = nE
        self.elements = elements
        self.nodes = nodes
        self.globalData = globalData


    def __str__(self):
        return (f"""
            nN = {self.nN}
            nE = {self.nE}
            elements = {self.elements}
            nodes = {self.nodes}
        """)

    def get_node_by_id(self, id):
        for node in self.nodes:
            if node.id == id:
                return node

    def calc_jacobian_and_h_for_elem(self):
        for element in self.elements:
            nodes = []
            for vert in element.vertices:
                nodes.append(self.get_node_by_id(vert))

            element.calculate_jacobian_and_h(nodes, self.globalData.conductivity)

    def calc_hbc_for_elem(self, alpha, tot):
        for element in self.elements:
            element.calculate_hbc(self.nodes, alpha, tot)

    def calc_c_for_elem(self, density, specific_heat):
        for element in self.elements:
            element.calculate_c(self.nodes, density, specific_heat)

    def display_jacobian_and_h_matrices(self):
        print("\nLocal Jacobian & H matrices for Each Element:")
        for element in self.elements:
            element.display_jacobian_and_h()

    def display_hbc_matrices(self):
        print("\nLocal Hbc Matrices and P Vectors for Each Element:")
        for element in self.elements:
            element.display_hbc_matrix()

    def display_c_matrices(self):
        print("\nLocal C Matrices for Each Element:")
        for element in self.elements:
            element.display_c_matrix()