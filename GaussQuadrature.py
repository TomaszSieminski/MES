import math
import numpy as np
import config

class GaussQuadrature:
    def __init__(self):
        self.pc_params = []
        self.weights = []

        self.set_gauss_points()

    def set_gauss_points(self):
        if config.pc_mode == 4:
            point = math.sqrt(1 / 3)
            self.pc_params = [[-point, -point],
                              [point, -point],
                              [point, point],
                              [-point, point]]
            self.weights = [1/1, 1/1]
        elif config.pc_mode == 9:
            point = math.sqrt(3 / 5)
            self.pc_params = [[-point, -point], [-point, 0], [-point, point],
                              [0, -point], [0, 0], [0, point],
                              [point, -point], [point, 0], [point, point]]
            self.weights = [5 / 9, 8 / 9, 5 / 9]
        elif config.pc_mode == 16:
            point1 = -0.8611363116
            point2 = -0.3399810436
            point3 = 0.3399810436
            point4 = 0.8611363116

            self.pc_params = [[point1, point1], [point1, point2], [point1, point3], [point1, point4],
                              [point2, point1], [point2, point2], [point2, point3], [point2, point4],
                              [point3, point1], [point3, point2], [point3, point3], [point3, point4],
                              [point4, point1], [point4, point2], [point4, point3], [point4, point4]]

            weight1 = 0.3478548451
            weight2 = 0.6521451549
            self.weights = [weight1, weight2, weight2, weight1,
                            weight2, weight2, weight2, weight2,
                            weight2, weight2, weight2, weight2,
                            weight1, weight2, weight2, weight1]
        else:
            self.pc_params = []

        self.weights = (self.weights * (np.array(self.weights)[np.newaxis].T)).flatten()


gauss = GaussQuadrature()