# GeoModeler/src/geometrycollection.py

from typing import Annotated, Union, List
from typing_extensions import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator
from .point import Point
from .linestring import LineString
from .polygon import Polygon
from .multipoint import MultiPoint
from .multilinestring import MultiLineString
from .multipolygon import MultiPolygon

class GeometryCollection(BaseModel, extra='forbid'):
    """
    A class used to represent a GeometryCollection in GeoJSON format.

    Attributes
    ----------
    type : Literal['GeometryCollection']
        A literal type indicating the GeoJSON object type. Always 'GeometryCollection' for this class.
    geometries : List[Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon]]
        A list of geometries. Each geometry must be a valid GeoJSON geometry object.

    Methods
    -------
    validate_geometries(v: List[Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon]])
        Validates the 'geometries' field. Raises a ValueError if the geometries are not valid.
    model_dump() -> dict
        Returns a dictionary representation of the model.
    model_dump_json() -> str
        Returns a GeoJSON string representation of the model.
    model_validate(v: dict)
        Validates a dictionary representation of the model. Raises a ValueError if the dictionary is not a valid GeometryCollection.

    Examples
    --------
    geometry_collection = GeometryCollection(type='GeometryCollection', geometries=[Point(type='Point', coordinates=[1.0, 2.0])])
    geometry_collection = GeometryCollection(geometries=[Point(type='Point', coordinates=[1.0, 2.0]), LineString(type='LineString', coordinates=[[3.0, 4.0], [5.0, 6.0]])])
    geometry_collection = GeometryCollection.model_validate({'type': 'GeometryCollection', 'geometries': [{'type': 'Point', 'coordinates': [1.0, 2.0]}, {'type': 'LineString', 'coordinates': [[3.0, 4.0], [5.0, 6.0]]}]})
    geometry_collection.model_dump_json() == '{"type":"GeometryCollection","geometries":[{"type":"Point","coordinates":[1.0,2.0]},{"type":"LineString","coordinates":[[3.0,4.0],[5.0,6.0]]}]}'
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    type: Annotated[Literal['GeometryCollection'], Field(default='GeometryCollection', title='Type',
                                                         description='A literal type indicating the GeoJSON object type. Always "GeometryCollection" for this class.')]
    geometries: Annotated[List[Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon]], Field(..., title='Geometries',
                                                                                                                   description='A list of geometries. Each geometry must be a valid GeoJSON geometry object.',
                                                                                                                   examples=[[{'type': 'Point', 'coordinates': [1.0, 2.0]}, {'type': 'LineString', 'coordinates': [[3.0, 4.0], [5.0, 6.0]]}]])]

    @field_validator('geometries', mode='after')
    @classmethod
    def validate_geometries(cls, v: List[Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon]]):
        """
        Validates the 'geometries' field.

        This method checks if the geometries provided are valid. It ensures that 'geometries' is a list and that each item in the list is a valid GeoJSON geometry object.

        Parameters
        ----------
        v : List[Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon]]
            The list of geometries to validate.

        Returns
        -------
        List[Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon]]
            The validated list of geometries.

        Raises
        ------
        ValueError
            If 'geometries' is not a list or if any item in the list is not a valid GeoJSON geometry object.
        """
        if not isinstance(v, list):
            raise ValueError("Geometries must be a list")

        if len(v) > 0:
            for geometry in v:
                if not isinstance(geometry, (Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon)):
                    raise ValueError("Geometries list must contain only Point, LineString, Polygon, MultiPoint, "
                                     "MultiLineString, or MultiPolygon objects")

        return v
