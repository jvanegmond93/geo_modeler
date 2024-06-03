# GeoModeler/src/utils.py
from typing import List, Union




def convert_to_float(coord: Union[float, str, int]):
    """
    Converts a coordinate to a float if it's a valid number string.

    Parameters
    ----------
    coord : Union[float, str, int]
        The coordinate to convert.

    Returns
    -------
    [float]
        The converted coordinate.
    """
    if isinstance(coord, str) and coord.replace('.', '', 1).isdigit():
        return float(coord)
    return coord


def calculate_area(linear_ring: List[List[float]]):
    area = 0.0
    for j in range(len(linear_ring) - 1):
        area += linear_ring[j][0] * linear_ring[j + 1][1] - linear_ring[j + 1][0] * linear_ring[j][1]
    area /= 2.0
    return area


