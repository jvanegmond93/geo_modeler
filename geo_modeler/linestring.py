# GeoModeler/geo_modeler/linestring.py
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Union, Annotated, Optional
from typing_extensions import Literal
from .utils import convert_to_float
from .validators import validate_point


class LineString(BaseModel, extra='forbid'):
    """
    A class used to represent a LineString in GeoJSON format.

    Attributes
    ----------
    type : Literal['LineString']
        A literal type indicating the GeoJSON object type. Always 'LineString' for this class.
    coordinates : List[List[float]]
        An array of points forming the LineString. Each point must be a valid set of coordinates.

    Methods
    -------
    validate_type(v: str)
        Validates the 'type' field. Raises a ValueError if the type is not 'LineString'.
    validate_coordinates(v: List[List[float]])
        Validates the 'coordinates' field. Raises a ValueError if the coordinates are not valid for a LineString.
    """

    model_config = ConfigDict()
    type: Annotated[Literal['LineString'], Field(default='LineString', title='Type',
                                                 description='A literal type indicating the GeoJSON object type. Always "LineString" for this class.',
                                                 examples=['LineString'])]
    coordinates: Annotated[List[List[float]], Field(..., title='Coordinates',
                                                    description='An array of points forming the LineString. Each point must be a valid set of coordinates.',
                                                    examples=[[[1.0, 2.0], [3.0, 4.0]]])]


    @field_validator('coordinates', mode='after')
    @classmethod
    def validate_coordinates(cls, v: List[List[float]]):
        """
        Validates the 'coordinates' field for a LineString.
        """
        if len(v) < 2:
            raise ValueError("LineString must have at least 2 points")

        for point in v:
            # Convert string coordinates to float if possible and validate each point
            converted_point = [convert_to_float(coord) for coord in point]
            validate_point(converted_point)

        return v

