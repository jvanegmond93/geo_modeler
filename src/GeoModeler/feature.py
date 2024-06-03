# GeoModeler/src/feature.py

from typing import Annotated, Any, Dict, Union, Optional, List, Literal

from pydantic import BaseModel, field_validator, Field, ConfigDict, BeforeValidator, AfterValidator

from GeoModeler import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection
from .validators import validate_bbox, type_validator

# FeatureType = Annotated[str, BeforeValidator(type_validator('Feature'))]
BBox = Annotated[Optional[List[float]], AfterValidator(validate_bbox)]


class Feature(BaseModel, extra='allow'):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: Annotated[Optional[Union[str, int]], Field(None, title='ID', description='The ID of the feature')]
    type: Literal['Feature'] = Field(default='Feature', title='Type',
                                        description='A literal type indicating the GeoJSON object type. '
                                                    'Always "Feature" for this class.')
    
    bbox: Annotated[BBox, Field(None,
                                title='Bounding Box (bbox)',
                                description="The Bounding Box (bbox) is a list of numbers conforming to values as "
                                            "described in RFC 7946.")]
    properties: Annotated[Optional[Dict[str, Any]], Field(None, title='Properties')]
    geometry: Annotated[
        Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection],
        Field(..., title='Geometry', discriminator='type')
    ]

    @field_validator('geometry', mode='after')
    def validate_geometry(cls, v: Union[
        Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection]):
        if not isinstance(v,
                          (Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection)):
            raise ValueError("Geometry must be a Point, MultiPoint, LineString, MultiLineString, Polygon, "
                             "MultiPolygon, or GeometryCollection object")

        return v
