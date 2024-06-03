# GeoModeler/src/utils.py
from typing import List, Union

def convert_to_float(coord: Union[float, str, int]) -> float:
    """
    Converts a coordinate to a float if it's a valid number string.

    This function checks if the input coordinate is a string that represents a valid number.
    If so, it converts the string to a float. Otherwise, it returns the coordinate as is.

    Parameters
    ----------
    coord : Union[float, str, int]
        The coordinate to convert. It can be of type float, string, or int.

    Returns
    -------
    float
        The converted coordinate as a float. If the input was already a float or int, it returns the input unchanged.

    Examples
    --------
    >>> convert_to_float('123.45')
    123.45
    >>> convert_to_float(123)
    123
    >>> convert_to_float('abc')
    'abc'
    """
    if isinstance(coord, str) and coord.replace('.', '', 1).isdigit():
        return float(coord)
    return coord

def calculate_area(linear_ring: List[List[float]]) -> float:
    """
    Calculates the area of a polygon defined by a linear ring using the Shoelace formula.

    This function computes the area of a polygon based on its linear ring coordinates.
    The Shoelace formula (Gauss's area formula) is used for the calculation.

    Parameters
    ----------
    linear_ring : List[List[float]]
        A list of points defining the linear ring of the polygon. Each point is a list of two floats [x, y].

    Returns
    -------
    float
        The calculated area of the polygon. The area is positive if the linear ring is oriented counter-clockwise, and negative if clockwise.

    Examples
    --------
    >>> calculate_area([[0.0, 0.0], [4.0, 0.0], [4.0, 3.0], [0.0, 3.0], [0.0, 0.0]])
    12.0
    """
    area = 0.0
    for j in range(len(linear_ring) - 1):
        area += linear_ring[j][0] * linear_ring[j + 1][1] - linear_ring[j + 1][0] * linear_ring[j][1]
    area /= 2.0
    return area
