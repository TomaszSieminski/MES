import numpy as np
from GaussQuadrature import gauss
from ShapeFunctionDerivatives import ShapeFunctionDerivatives
from numpy.linalg import det, inv

class Jacobian:
    def __init__(self, nodes, k):
        self.j = []
        self.j1 = []
        self.detJ = []
        self.dN_dX = []
        self.dN_dY = []

        pc_params = gauss.pc_params

        dN_dKsi = [[ShapeFunctionDerivatives.dN1_dKsi(param[1]),
                    ShapeFunctionDerivatives.dN2_dKsi(param[1]),
                    ShapeFunctionDerivatives.dN3_dKsi(param[1]),
                    ShapeFunctionDerivatives.dN4_dKsi(param[1])] for param in pc_params]

        dN_dEta = [[ShapeFunctionDerivatives.dN1_dEta(param[0]),
                    ShapeFunctionDerivatives.dN2_dEta(param[0]),
                    ShapeFunctionDerivatives.dN3_dEta(param[0]),
                    ShapeFunctionDerivatives.dN4_dEta(param[0])] for param in pc_params]

        for i in range(len(dN_dKsi)):
            self.j.append([
                [
                    sum(dN_dKsi[i][j] * nodes[j].x for j in range(len(dN_dKsi[0]))),
                    sum(dN_dKsi[i][j] * nodes[j].y for j in range(len(dN_dKsi[0])))
                ],
                [
                    sum(dN_dEta[i][j] * nodes[j].x for j in range(len(dN_dEta[0]))),
                    sum(dN_dEta[i][j] * nodes[j].y for j in range(len(dN_dEta[0])))
                ]
            ])

        for row in self.j:
            self.detJ.append(det(row))

        for row in self.j:
            self.j1.append(inv(row))

        # Compute dN_dX and dN_dY
        for i in range(len(dN_dKsi)):
            temp1 = []
            temp2 = []

            for j in range(len(dN_dKsi[0])):
                temp1.append(float(dN_dKsi[i][j] * self.j1[i][0][0] + dN_dEta[i][j] * self.j1[i][0][1]))
                temp2.append(float(dN_dKsi[i][j] * self.j1[i][1][0] + dN_dEta[i][j] * self.j1[i][1][1]))

            self.dN_dX.append(temp1)
            self.dN_dY.append(temp2)



    def __str__(self):
        np.set_printoptions(precision=5, linewidth=120, suppress=True)

        print("Jakobian: ")
        for i in  range(len(self.j)):
            print("J" + str(i+1) + ":")
            for row in self.j[i]:
                print(row)

        print("Jakobian^-1:")
        for i in  range(len(self.j1)):
            print("J_1(" + str(i+1) + "):")
            for row in self.j1[i]:
                print(row)

        print("detJ:")
        for i in range(len(self.detJ)):
            print("detJ(" + str(i+1) + "):", self.detJ[i])

        print("dN_dX:")
        for i in range(len(self.dN_dX)):
            print("dN_dX(" + str(i + 1) + "):", self.dN_dX[i])

        print("dN_dY:")
        for i in range(len(self.dN_dY)):
            print("dN_dY(" + str(i + 1) + "):", self.dN_dY[i])


        print("\n")





