# GeoModeler/src/geometrycollection.py

from typing import Annotated, Union
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict, field_validator

from src import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon


class GeometryCollection(BaseModel, extra='forbid'):
    """
    A class used to represent a GeometryCollection in GeoJSON format.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    type: Annotated[Literal['GeometryCollection'], Field(default='GeometryCollection', title='Type')]
    geometries: list[Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon]]

    @field_validator('geometries', mode='after')
    def validate_geometries(cls, v: list[Union[Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon]]):
        # Validation logic for geometries
        # Ensure that all items in the list are instances of the geometry models
        if not isinstance(v, list):
            raise ValueError("Geometries must be a list")

        if len(v) > 0:
            for geometry in v:
                if not isinstance(geometry, (Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon)):
                    raise ValueError("Geometries list must contain only Point, LineString, Polygon, MultiPoint, "
                                     "MultiLineString, or MultiPolygon objects")

        return v

