# GeoModeler/src/multipoint.py
from pydantic import field_validator
from typing import List, Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Literal
from .utils import convert_to_float
from .validators import validate_point


class MultiPoint(BaseModel, extra='forbid'):
    """
    A class used to represent a MultiPoint in GeoJSON format.

    Attributes
    ----------

    type : Literal['MultiPoint']
        A literal type indicating the GeoJSON object type. Always 'MultiPoint' for this class.
    coordinates : List[List[float]]
        A list of Point coordinate arrays. Each point must be a valid set of coordinates.

    Methods
    -------
    validate_type(v: str)
        Validates the 'type' field. Raises a ValueError if the type is not 'MultiPoint'.

    model_dump() -> dict
        Returns a dictionary representation of the model.
    model_dump_json() -> str
        Returns a GeoJSON string representation of the model.

    validate_coordinates(v: List[List[float]])
        Validates the 'coordinates' field. Raises a ValueError if the coordinates are not a valid set of coordinates.

    model_validate(v: dict)
        Validates a dictionary representation of the model. Raises a ValueError if the dictionary is not a valid MultiPoint.

    model_validate_json(v: str)
        Validates a GeoJSON string representation of the model. Raises a ValueError if the string is not a valid MultiPoint.


    Examples
    --------
    multi_point = MultiPoint(type='MultiPoint', coordinates=[[1.0, 2.0], [3.0, 4.0]])
    multi_point = MultiPoint(coordinates=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    multi_point = MultiPoint.validate_json('{"type":"MultiPoint","coordinates":[[1.0,2.0,3.0],[4.0,5.0,6.0]]}')
    multi_point.model_dump_json() == '{"type":"MultiPoint","coordinates":[[1.0,2.0,3.0],[4.0,5.0,6.0]]}'
    """

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True)
    type: Annotated[Literal['MultiPoint'], Field(default='MultiPoint', title='Type',
                                                 description='A literal type indicating the GeoJSON object type. '
                                                             'Always "MultiPoint" for this class.',
                                                 examples=['MultiPoint'])]
    coordinates: Annotated[List[List[float]], Field(...,
                                                    title="Coordinates",
                                                    description="A list of Point coordinate arrays. Each point must "
                                                                "be a valid set of coordinates.",
                                                    examples=[[0.0, 0.0], [1.1, 1.1, 1.1]])]



    @field_validator('coordinates', mode='after')
    def validate_coordinates(cls, v: List[List[float]]):
        """
        Validates the 'coordinates' field.

        This method ensures that each point in the coordinates list has either 2 or 3 numeric elements
        (longitude, latitude, [elevation]).

        Parameters
        ----------
        v : List[List[float]]
            The list of coordinates to validate.

        Returns
        -------
        List[List[float]]
            The validated coordinates.

        Raises
        ------
        ValueError
            If any point does not have exactly 2 or 3 numeric elements or if the coordinates are empty.
        """

        if not isinstance(v, list) or not v:
            raise ValueError("Coordinates must be a non-empty list of coordinate lists")
        if not all(isinstance(point, list) for point in v):
            raise ValueError("Each coordinate must be a list")

        for point in v:
            # Convert string coordinates to float if possible and validate each point
            coordinates = [convert_to_float(coord) for coord in point]
            validate_point(coordinates) # Raises ValueError if the point is invalid

        return v