import numpy as np
from numpy import cos, sin


def rot1(alpha: float) -> np.ndarray:
    cos_a = cos(alpha)
    sin_a = sin(alpha)
    return np.array([[1, 0, 0], [0, cos_a, sin_a], [0, -sin_a, cos_a]])


def rot2(alpha: float) -> np.ndarray:
    cos_a = cos(alpha)
    sin_a = sin(alpha)
    return np.array([[cos_a, 0, -sin_a], [0, 1, 0], [sin_a, 0, cos_a]])


def rot3(alpha: float) -> np.ndarray:
    cos_a = cos(alpha)
    sin_a = sin(alpha)
    return np.array([[cos_a, sin_a, 0], [-sin_a, cos_a, 0], [0, 0, 1]])
