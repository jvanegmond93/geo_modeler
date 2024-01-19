# GeoModeler/geo_modeler/polygon.py

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Annotated, Optional
from typing_extensions import Literal
from .utils import convert_to_float, calculate_area
from .validators import validate_point, validate_linear_ring, validate_ring_orientation


class Polygon(BaseModel, extra='forbid'):
    """
    A class used to represent a Polygon in GeoJSON format.

    Attributes
    ----------
    type : Literal['Polygon']
        A literal type indicating the GeoJSON object type. Always 'Polygon' for this class.
    coordinates : List[List[List[float]]]
        A list of linear rings forming the Polygon. The first linear ring is the exterior ring, and any subsequent rings are interior rings (holes). Each linear ring must be a valid set of coordinates.

    Methods
    -------
    validate_type(v: str)
        Validates the 'type' field. Raises a ValueError if the type is not 'Polygon'.
    validate_coordinates(v: List[List[List[float]]])
        Validates the 'coordinates' field. Raises a ValueError if the coordinates are not valid for a Polygon.

    Examples
    --------
    polygon = Polygon(type='Polygon', coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]])
    polygon = Polygon(coordinates=[[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0], [1.0, 2.0, 3.0]], [[10.0, 11.0, 12.0], [13.0, 14.0, 15.0], [16.0, 17.0, 18.0], [10.0, 11.0, 12.0]]])
    polygon = Polygon.validate_json('{"type":"Polygon","coordinates":[[[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0],[1.0,2.0,3.0]],[[10.0,11.0,12.0],[13.0,14.0,15.0],[16.0,17.0,18.0],[10.0,11.0,12.0]]]}')
    polygon.model_dump_json() == '{"type":"Polygon","coordinates":[[[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0],[1.0,2.0,3.0]],[[10.0,11.0,12.0],[13.0,14.0,15.0],[16.0,17.0,18.0],[10.0,11.0,12.0]]]}'
    """

    model_config = ConfigDict()
    type: Literal['Polygon'] = Field(default='Polygon', title='Type',
                                     description='A literal type indicating the GeoJSON object type. '
                                                 'Always "Polygon" for this class.',
                                     examples=['Polygon'])
    coordinates: Annotated[List[List[List[float]]], Field(..., title='Coordinates',
                                                          description='A list of linear rings forming the Polygon. The first linear ring is the exterior ring, and any subsequent rings are interior rings (holes). Each linear ring must be a valid set of coordinates.',
                                                          examples=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]])]

    @field_validator('coordinates', mode='after')
    def validate_coordinates(cls, v: List[List[List[float]]]):
        """
        Validates the 'coordinates' field for a Polygon.
        """
        if not v:
            raise ValueError("Coordinates cannot be empty")

        for i, linear_ring in enumerate(v):
            validate_linear_ring(linear_ring)
            area = calculate_area(linear_ring)
            validate_ring_orientation(i, area)

            for point in linear_ring:
                converted_point = [convert_to_float(coord) for coord in point]
                validate_point(converted_point)
        return v

