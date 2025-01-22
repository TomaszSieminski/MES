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
        else:
            self.pc_params = []

        self.weights = (self.weights * (np.array(self.weights)[np.newaxis].T)).flatten()

    def get_pc_params(self):
        return self.pc_params

    def get_weights(self):
        return self.weights