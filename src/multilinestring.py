# GeoModeler/src/multilinestring.py
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Annotated, Optional
from typing_extensions import Literal
from .utils import convert_to_float
from .validators import validate_point


class MultiLineString(BaseModel, extra='forbid'):
    """
    A class used to represent a MultiLineString in GeoJSON format.

    Attributes
    ----------
    type : Literal['MultiLineString']
        A literal type indicating the GeoJSON object type. Always 'MultiLineString' for this class.
    coordinates : List[List[List[float]]]
        A list of LineString coordinate arrays. Each LineString must be a valid set of coordinates.

    Methods
    -------
    validate_type(v: str)
        Validates the 'type' field. Raises a ValueError if the type is not 'MultiLineString'.
    validate_coordinates(v: List[List[List[float]]])
        Validates the 'coordinates' field. Raises a ValueError if the coordinates are not valid for a MultiLineString.

    Examples
    --------
    multi_line_string = MultiLineString(type='MultiLineString', coordinates=[[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])
    multi_line_string = MultiLineString(coordinates=[[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], [[7.0, 8.0, 9.0], [10.0, 11.0, 12.0]]])
    multi_line_string = MultiLineString.validate_json('{"type":"MultiLineString","coordinates":[[[1.0,2.0,3.0],[4.0,5.0,6.0]],[[7.0,8.0,9.0],[10.0,11.0,12.0]]]}')
    multi_line_string.model_dump_json() == '{"type":"MultiLineString","coordinates":[[[1.0,2.0,3.0],[4.0,5.0,6.0]],[[7.0,8.0,9.0],[10.0,11.0,12.0]]]}'
    """

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        str_strip_whitespace=True)
    type: Annotated[Literal['MultiLineString'], Field(default='MultiLineString', title='Type',
                                                      description='A literal type indicating the GeoJSON object type. '
                                                                  'Always "MultiLineString" for this class.',
                                                      examples=['MultiLineString'])]
    coordinates: Annotated[List[List[List[float]]], Field(..., title='Coordinates',
                                                          description='A list of LineString coordinate arrays. Each '
                                                                      'LineString must be a valid set of coordinates.',
                                                          examples=[[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])]



    @field_validator('coordinates', mode='after')
    def validate_coordinates(cls, v: List[List[List[float]]]):
        """
        Validates the 'coordinates' field for a MultiLineString.
        """
        if not v:
            raise ValueError("Coordinates cannot be empty")

        for linestring in v:
            if len(linestring) < 2:
                raise ValueError("Each LineString in a MultiLineString must have at least 2 points")

            for point in linestring:
                # Convert string coordinates to float if possible and validate each point
                converted_point = [convert_to_float(coord) for coord in point]
                validate_point(converted_point)

        return v
