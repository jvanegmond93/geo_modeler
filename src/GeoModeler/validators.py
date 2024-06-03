import warnings
from typing import Union, Tuple, Optional, List, Annotated



def validate_point_coordinates(coordinates: Union[Tuple[float, float, Optional[float]], List[float]]):
    # Convert string coordinates to float if possible
    coordinates: List = [float(coord) if isinstance(coord, str) and coord.replace('.', '', 1).isdigit() else coord for
                         coord
                         in coordinates]

    if len(coordinates) not in [2, 3]:
        raise ValueError("Coordinates must have 2 or 3 elements (longitude, latitude, [elevation])")
    if not all(isinstance(coord, (float, int)) for coord in coordinates):
        raise ValueError("All coordinate values must be numeric")
    return coordinates


# Validator for MultiPoint coordinates
def validate_multipoint_coordinates(coordinates: List[Union[Tuple[float, float, Optional[float]], List[float]]]):
    if not isinstance(coordinates, list) or not all(isinstance(coord, (list, tuple)) for coord in coordinates):
        raise ValueError("Coordinates for MultiPoint must be a list of coordinate tuples/lists")

    return [validate_point_coordinates(coord) for coord in coordinates]


# Validator for LineString coordinates
def validate_linestring_coordinates(coordinates: List[Union[Tuple[float, float, Optional[float]], List[float]]]):
    validated_coords = validate_multipoint_coordinates(coordinates)

    if len(validated_coords) < 2:
        raise ValueError("Coordinates for LineString must contain at least two points")

    return validated_coords

#
def validate_point(point: List[float]):
    """
    Validates a single point's coordinates.

    Parameters
    ----------
    point : List[Union[float]]
        The coordinates of the point to validate.

    Raises
    ------
    ValueError
        If the point does not have 2 or 3 elements or if any coordinate is not numeric.
    """
    if len(point) not in [2, 3]:
        raise ValueError("Each point must have 2 or 3 elements (longitude, latitude, [elevation])")
    if not all(isinstance(coord, (float, int)) for coord in point):
        raise ValueError("All coordinate values in the point must be numeric")


def validate_linear_ring(linear_ring: List[List[float]]):
    if len(linear_ring) < 4:
        raise ValueError(
            "Each linear ring in a Polygon must have at least 4 points (including the closing point)")

    if linear_ring[0] != linear_ring[-1] or type(linear_ring[0]) is not type(linear_ring[-1]):
        raise ValueError(
            "Each linear ring in a Polygon must close by repeating the first point with identical representation")



def validate_ring_orientation(i: int, area: float, warn: bool = True):
    if i == 0 and area <= 0:  # exterior ring
        message = "The exterior ring must be counterclockwise"
        if warn:
            warnings.warn(message)
        else:
            raise ValueError(message)
    elif i > 0 and area >= 0:  # interior rings
        message = "The interior rings must be clockwise"
        if warn:
            warnings.warn(message)
        else:
            raise ValueError(message)

class RingDirectionWarning(Warning):
    pass
def validate_bbox(values: List[float]) -> List[float]:
    n = len(values) // 2
    if len(values) % 2 != 0 or n not in [2, 3]:  # Supports 2D or 3D bbox only
        raise ValueError("bbox must be an array of length 4 (2D) or 6 (3D)")

    west, south, east, north = values[:4]

    # Check for antimeridian crossing
    if east < west:
        if not (-180 <= west <= 180 and -180 <= east <= 180):
            raise ValueError("Longitude values must be between -180 and 180 when crossing the antimeridian")

    # Normal longitude check when not crossing the antimeridian
    elif not -180 <= west <= 180 or not -180 <= east <= 180:
        raise ValueError("Longitude values must be between -180 and 180")

    # Latitude checks
    if not -90 <= south <= 90 or not -90 <= north <= 90:
        raise ValueError("Latitude values must be between -90 and 90")

    # Check if latitude values are in correct order
    if south > north:
        raise ValueError("South latitude must be less than or equal to north latitude")
    return values


def type_validator(type_name: str):
    def validate(v: str) -> str:
        if v.lower() != type_name.lower():
            raise ValueError(f"Type must be '{type_name}'")
        return v

    return validate
