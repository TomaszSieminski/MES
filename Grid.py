from Jacobian import Jacobian
from MatrixH import MatrixH
from MatrixHbc import MatrixHbc

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
        self.jacobian = []
        self.Hbc = []

    def calculate_hbc(self, nodes, alpha, tot):
        element_nodes = [nodes[node_id - 1] for node_id in self.vertices]
        matrix_hbc = MatrixHbc(element_nodes, alpha, tot)
        self.Hbc = matrix_hbc.Hbc
        self.P_local = matrix_hbc.P_local

    def display_hbc_matrix(self):
        print(f"Element {self.id}:")
        print("Hbc Matrix:")
        for row in self.Hbc:
            print("  ", "  ".join(f"{value:.4f}" for value in row))
        print("P Vector:")
        print("  ", "  ".join(f"{value:.4f}" for value in self.P_local))
        print()

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

    def calc_jacobian_and_H_for_elem(self):
        for element in self.elements:
            nodes = []
            for vert in element.vertices:
                nodes.append(self.get_node_by_id(vert))

            element.jacobian = Jacobian(nodes, self.globalData.conductivity)
            #print("Element", element.id)
            #element.jacobian.__str__()

            element.matrixH = MatrixH(element.jacobian, self.globalData.conductivity)

    def calc_hbc_for_elem(self, alpha, tot):
        for element in self.elements:
            element.calculate_hbc(self.nodes, alpha, tot)


    def display_hbc_matrices(self):
        print("\nLocal Hbc Matrices and P Vectors for Each Element:")
        for element in self.elements:
            element.display_hbc_matrix()