import numpy as np


# returns the distance between two points in tuple notation
def distance(p1, p2):
    v = np.subtract(p1, p2)
    return np.linalg.norm(v)
