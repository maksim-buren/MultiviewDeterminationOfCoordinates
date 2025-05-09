import numpy as np


class ViewCoordinateDetermination:

    def __init__(self, scale: float, center: tuple[int, int], K: np.array, R: np.array, T: np.array):
        self.scale = scale
        self.cx, self.cy = center
        self.K = K
        self.R = R
        self.T = T
        self.A = self.K @ self.R
        self.KRT = self.K @ self.R @ self.T

    def get_coordinates_by_pixel(self, x: float, y: float) -> tuple[float, float]:
        x_scaled = x * self.scale
        y_scaled = y * self.scale
        new_column = np.array([[self.cx - x_scaled], [self.cy - y_scaled], [-1]])
        a_modified = np.hstack((self.A[:, :2], new_column))
        p = np.linalg.lstsq(a_modified, self.KRT, rcond=None)[0]
        return p[0, 0], p[1, 0]
