class Surface:
    def __init__(self, num_points):
        self.N = [[0.0] * 4 for _ in range(num_points)]

    def get_N(self):
        return self.N
