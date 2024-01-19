# GeoModeler/geo_modeler/multipolygon.py

from typing import List, Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing_extensions import Literal
from .utils import calculate_area, convert_to_float
from .validators import validate_point, validate_linear_ring, validate_ring_orientation


class MultiPolygon(BaseModel, extra='forbid'):
    """
    A class used to represent a MultiPolygon in GeoJSON format.

    Attributes
    ----------
    type : Literal['MultiPolygon']
        A literal type indicating the GeoJSON object type. Always 'MultiPolygon' for this class.
    coordinates : List[List[List[List[float]]]]
        A list of polygons where each polygon is represented as a list of linear rings. The first linear ring in each polygon is the exterior ring, with any subsequent rings representing interior rings (holes).

    Methods
    -------
    validate_type(v: str)
        Validates the 'type' field. Raises a ValueError if the type is not 'MultiPolygon'.
    validate_coordinates(v: List[List[List[List[float]]]])
        Validates the 'coordinates' field. Raises a ValueError if the coordinates are not valid for a MultiPolygon.

    Examples
    --------
    multipolygon = MultiPolygon(type='MultiPolygon', coordinates=[[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]])
    multipolygon = MultiPolygon(coordinates=[[[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0], [1.0, 2.0, 3.0]]], [[[10.0, 11.0, 12.0], [13.0, 14.0, 15.0], [16.0, 17.0, 18.0], [10.0, 11.0, 12.0]]]])
    multipolygon = MultiPolygon.validate_json('{"type":"MultiPolygon","coordinates":[[[[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0],[1.0,2.0,3.0]]],[[[10.0,11.0,12.0],[13.0,14.0,15.0],[16.0,17.0,18.0],[10.0,11.0,12.0]]]]}')
    multipolygon.model_dump_json() == '{"type":"MultiPolygon","coordinates":[[[[1.0,2.0,3.0],[4.0,5.0,6.0],[7.0,8.0,9.0],[1.0,2.0,3.0]]],[[[10.0,11.0,12.0],[13.0,14.0,15.0],[16.0,17.0,18.0],[10.0,11.0,12.0]]]]}'
    """

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)
    type: Literal['MultiPolygon'] = Field(default='MultiPolygon', title='Type',
                                            description='A literal type indicating the GeoJSON object type. '
                                                        'Always "MultiPolygon" for this class.',
                                            examples=['MultiPolygon'])
    coordinates: Annotated[List[List[List[List[float]]]], Field(..., title='Coordinates',validate_default=True,
                                                                description='A list of polygons, each represented as '
                                                                            'a list of linear rings. The first linear '
                                                                            'ring in each'
                                                                            'polygon is the exterior ring, with '
                                                                            'subsequent rings being interior rings ('
                                                                            'holes).', examples=[
            [[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]])]


    @field_validator('coordinates', mode='after')
    def validate_coordinates(cls, v: List[List[List[List[float]]]]):
        """
        Validates the 'coordinates' field for a MultiPolygon.
        """
        if not isinstance(v, list) or not v:
            raise ValueError("Coordinates must be a list of polygons and cannot be empty")

        for i, polygon in enumerate(v):
            if not isinstance(polygon, list) or not polygon:
                raise ValueError(f"Polygon {i} must be a list of linear rings and cannot be empty")

            for j, linear_ring in enumerate(polygon):
                validate_linear_ring(linear_ring)
                area = calculate_area(linear_ring)
                validate_ring_orientation(j, area)

                for point in linear_ring:
                    converted_point = [convert_to_float(coord) for coord in point]
                    validate_point(converted_point)

        return v
