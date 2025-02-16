import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np


class GridPlotter:
    def __init__(self, grid):
        self.grid = grid

    def plot_grid(self):
        fig, ax = plt.subplots()

        # Rysowanie elementów (czworoboków)
        for element in self.grid.elements:
            nodes = [self.grid.get_node_by_id(node_id) for node_id in element.vertices]
            x_coords = [node.x for node in nodes]
            y_coords = [node.y for node in nodes]
            polygon = Polygon(list(zip(x_coords, y_coords)), edgecolor='black', facecolor='skyblue', linewidth=1, alpha=0.6)
            ax.add_patch(polygon)

            # Obliczanie środka elementu i dodawanie etykiety
            center_x = np.mean(x_coords)
            center_y = np.mean(y_coords)
            ax.annotate(f"E{element.id}", (center_x, center_y), color='black', ha='center', va='center', fontsize=8)

        # Rysowanie i numerowanie węzłów
        for node in self.grid.nodes:
            color = 'red' if node.BC == 1 else 'black'
            ax.plot(node.x, node.y, marker='o', markersize=5, color=color)

        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.axis('off')

        plt.show()