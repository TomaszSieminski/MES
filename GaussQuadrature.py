import numpy as np
import config
from numpy.polynomial.legendre import leggauss

class GaussQuadrature:
    def __init__(self):
        self.pc_params = []
        self.weights = []

        self.set_gauss_points()

    def set_gauss_points(self):
        if config.pc_mode in [4, 9, 16]: #użyj leggauss dla pc_mode == 4,9,16
            # 1. Generuj punkty i wagi Gaussa 1D
            points_1d, weights_1d = leggauss(config.pc_mode)

            # 2. Stwórz siatkę punktów 2D (iloczyn tensorowy)
            self.pc_params = [(x, y) for x in points_1d for y in points_1d]

            # 3. Oblicz wagi 2D
            self.weights = [w1 * w2 for w1 in weights_1d for w2 in weights_1d]

        else:
            self.pc_params = []
            self.weights = []


gauss = GaussQuadrature()