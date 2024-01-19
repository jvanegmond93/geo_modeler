# GeoModeler/src/point.py
from typing import List, Annotated, Optional
from pydantic import ConfigDict, BaseModel, field_validator
from pydantic import Field
from typing_extensions import Literal
from .utils import convert_to_float
from .validators import validate_point


class Point(BaseModel, extra='forbid'):
    """
    A class used to represent a Point in GeoJSON format.

    Attributes
    ----------

    type : Literal['Point']
        A literal type indicating the GeoJSON object type. Always 'Point' for this class.
    coordinates : List[float]
        The coordinates of the point. Must be a valid set of coordinates.

    Methods
    -------
    validate_type(v: str)
        Validates the 'type' field. Raises a ValueError if the type is not 'Point'.

    model_dump() -> dict
        Returns a dictionary representation of the model.
    model_dump_json() -> str
        Returns a GeoJSON string representation of the model.

    validate_coordinates(v: List[float])
        Validates the 'coordinates' field. Raises a ValueError if the coordinates are not a valid set of coordinates.

    model_validate(v: dict)
        Validates a dictionary representation of the model. Raises a ValueError if the dictionary is not a valid Point.

    Examples
    --------
    multi_point = MultiPoint(type='MultiPoint', coordinates=[[1.0, 2.0], [3.0, 4.0]])
    multi_point = MultiPoint(coordinates=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    multi_point = MultiPoint.validate_json('{"type":"MultiPoint","coordinates":[[1.0,2.0,3.0],[4.0,5.0,6.0]]}')
    multi_point.model_dump_json() == '{"type":"MultiPoint","coordinates":[[1.0,2.0,3.0],[4.0,5.0,6.0]]}'

    """


    model_config = ConfigDict(
        populate_by_name=True,
)
    type: Literal['Point'] = Field(default='Point', title='Type',
                                      description='A literal type indicating the GeoJSON object type. '
                                                  'Always "Point" for this class.',
                                      examples=['Point'])
    coordinates: Annotated[List[float], Field(..., title='Coordinates',
                                              description='The coordinates of the point. Must be a valid set of coordinates.',
                                              examples=[[1.0, 2.0], [3.0, 4.0]])]


    @field_validator('coordinates', mode='before')
    def validate_coordinates(cls, v: List[float]):
        """
        Validates the 'coordinates' field.

        This method checks if the coordinates provided are valid. It first converts any string coordinates to float values if possible.
        Then it checks if the length of the coordinates is either 2 or 3, as a valid set of coordinates must have 2 or 3 elements (longitude, latitude, [elevation]).
        Finally, it checks if all coordinate values are numeric (either float or int).

        Parameters
        ----------
        v : List[float]
            The list of coordinates to validate.

        Returns
        -------
        List
            The validated coordinates.

        Raises
        ------
        ValueError
            If the coordinates do not have 2 or 3 elements or if any of the coordinate values are not numeric.
        """

        # Convert string coordinates to float if possible and validate each point
        coordinates = [convert_to_float(coord) for coord in v]
        validate_point(coordinates)

        return coordinates
