import math


def vect(pt_1:list, pt_2:list):
    """
    Returns the vector from 2 points.
    """

    vector = list()
    for a, b in zip(pt_1, pt_2):
        vector.append(b - a)

    return vector


def norm(array:list):
    """
    Returns the 2-norm of an array.
    """

    val = 0
    for x in array:
        val += x**2

    return math.sqrt(val)
