from numpy.polynomial.legendre import leggauss
from config import pc_mode


class GaussQuadrature:
    def __init__(self):
        self.pc_params_1d = []
        self.weights_1d = []
        self.pc_params = []
        self.weights = []

        self.set_gauss_points()

    def set_gauss_points(self):
        points_1d, weights_1d = leggauss(pc_mode)
        self.pc_params_1d = points_1d
        self.weights_1d = weights_1d

        self.pc_params = [(x, y) for x in points_1d for y in points_1d]
        self.weights = [w1 * w2 for w1 in weights_1d for w2 in weights_1d]

gauss = GaussQuadrature()