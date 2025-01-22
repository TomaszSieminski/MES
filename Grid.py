from Jacobian import Jacobian
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
        self.jacobian = None
        self.Hbc = []

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

    def calc_jacobian_for_elem(self):
        for element in self.elements:
            nodes = []
            for vert in element.vertices:
                nodes.append(self.get_node_by_id(vert))

            element.jacobian = Jacobian(nodes, self.globalData.conductivity)
            #print("Element", element.id)
            #element.jacobian.__str__()

    def calc_Hbc_for_elem(self):
        for element in self.elements:
            matrix_hbc = MatrixHbc(self.globalData, self, element)
            element.Hbc = matrix_hbc.get_Hbc()
            element.P = matrix_hbc.get_P()

            print(f"Macierz Hbc dla elementu {element.id}:")
            for row in element.Hbc:
                print(row)
            print(f"Wektor P dla elementu {element.id}:")
            print(element.P)
