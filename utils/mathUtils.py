import numpy as np


# returns the distance between two points in tuple notation
def distance(p1, p2):
    v = np.subtract(p1, p2)
    return np.linalg.norm(v)


# return the direction in the unit circle
def get_direction(angle):
    rad_angle = np.deg2rad((angle + 90) % 360)
    return np.round(np.cos(rad_angle), 5), np.round(np.sin(rad_angle), 5)
