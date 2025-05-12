import numpy as np


class RotationMatrix:

    @staticmethod
    def rotation_matrix_y(theta_degrees):
        theta = np.radians(theta_degrees)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        return np.array([
            [cos_theta, 0, sin_theta],
            [0, 1, 0],
            [-sin_theta, 0, cos_theta]
        ])

    @staticmethod
    def rotation_matrix_z(theta_degrees):
        theta = np.radians(theta_degrees)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        return np.array([
            [cos_theta, -sin_theta, 0],
            [sin_theta, cos_theta, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def rotation_matrix_x(theta_degrees):
        theta = np.radians(theta_degrees)
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        return np.array([
            [1, 0, 0],
            [0, cos_theta, -sin_theta],
            [0, sin_theta, cos_theta]
        ])

    @staticmethod
    def euler_rotation_matrix(alpha, beta, gamma):
        Rz = RotationMatrix.rotation_matrix_z(alpha)
        Ry = RotationMatrix.rotation_matrix_y(beta)
        Rx = RotationMatrix.rotation_matrix_x(gamma)
        return Rz @ Ry @ Rx
