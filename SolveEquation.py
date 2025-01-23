import numpy as np


class SolveEquation:
    @staticmethod
    def solve(A, b):
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)

        # Augment the matrix A with vector b
        n = len(b)
        augmented_matrix = np.hstack((A, b.reshape(-1, 1)))

        # Gaussian elimination
        for i in range(n):
            # Normalize the pivot row
            augmented_matrix[i] = augmented_matrix[i] / augmented_matrix[i, i]

            # Eliminate the current column from the other rows
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j, i]
                    augmented_matrix[j] -= factor * augmented_matrix[i]

        # Extract the solution
        x = augmented_matrix[:, -1]
        return x
