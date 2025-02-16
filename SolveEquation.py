import numpy as np

class SolveEquation:
    @staticmethod
    def solve(A, b):
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)

        n = len(b)
        augmented_matrix = np.hstack((A, b.reshape(-1, 1)))

        for i in range(n):
            augmented_matrix[i] = augmented_matrix[i] / augmented_matrix[i, i]

            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j, i]
                    augmented_matrix[j] -= factor * augmented_matrix[i]

        x = augmented_matrix[:, -1]
        return x
