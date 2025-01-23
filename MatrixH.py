import numpy as np
from GaussQuadrature import gauss

class MatrixH:
    def __init__(self, jacobian, k):
        self.jacobian = jacobian
        self.Hpc = []
        self.H = []
        self.weights = gauss.weights

        self.compute_h_matrix(k)

    def compute_h_matrix(self, k):
        dN_dX, dN_dY = self.jacobian.dN_dX, self.jacobian.dN_dY
        detJ = self.jacobian.detJ

        for i in range(len(dN_dX)):
            hpc = k * ((dN_dX[i] * np.array(dN_dX[i])[np.newaxis].T) +
                       (dN_dY[i] * np.array(dN_dY[i])[np.newaxis].T)) * detJ[i]
            self.Hpc.append(hpc)

        self.H = sum(hpc * w for hpc, w in zip(self.Hpc, self.weights))