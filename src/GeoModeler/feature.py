# GeoModeler/src/feature.py

from typing import Annotated, Any, Dict, Union, Optional, List, Literal

from pydantic import BaseModel, field_validator, Field, ConfigDict, BeforeValidator, AfterValidator

from GeoModeler import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection
from .validators import validate_bbox, type_validator

# FeatureType = Annotated[str, BeforeValidator(type_validator('Feature'))]
BBox = Annotated[Optional[List[float]], AfterValidator(validate_bbox)]


class Feature(BaseModel, extra='allow'):
    """
    A class used to represent a Feature in GeoJSON format.

    A GeoJSON Feature represents a geographic object with properties. This class defines the structure
    and validation rules for a Feature.

    Attributes
    ----------
    id: Union[str, int] (optional)
        A unique identifier for the feature.

    type: Literal['Feature']
        A literal type indicating the GeoJSON object type. Always 'Feature' for this class.

    bbox: List[float] (optional)
        A list of coordinates representing the bounding box of the feature.

    properties: Dict[str, Any] (optional)
        A dictionary containing additional properties associated with the feature.

    geometry: Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection]
        The geometry associated with the feature. It can be any of the specified GeoJSON geometry types.

    Methods
    -------
    validate_type(v: str)
        Validates the 'type' field. Raises a ValueError if the type is not 'Feature'.

    model_dump() -> dict
        Returns a dictionary representation of the Feature model.

    model_dump_json() -> str
        Returns a GeoJSON string representation of the Feature model.

    validate_coordinates(v: Union[Point, MultiPoint, ...])
        Validates the geometry contained within the Feature.

    model_validate(v: dict)
        Validates a dictionary representation of the Feature model.
        Raises a ValueError if the dictionary is not a valid Feature.

    Examples
    --------
    # Create a Feature with a Point geometry:
    point_feature = Feature(geometry=Point(coordinates=[-122.6764, 45.5165]), properties={"name": "Portland"})

    # Create a Feature with a Polygon geometry and properties:
    polygon_feature = Feature(geometry=Polygon(...), properties={"population": 2000000})
    """

    model_config = ConfigDict(populate_by_name=True)

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

    @field_validator("geometry", mode="after")
    def validate_geometry(cls, v: Union[
        Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection]
                          ):
        """
        Validates the geometry contained within the Feature.

        This method ensures that the geometry provided is one of the valid GeoJSON geometry types.
        """

        if not isinstance(v, (
                Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection
        )):
            raise ValueError(
                "Geometry must be a Point, MultiPoint, LineString, MultiLineString, Polygon, "
                "MultiPolygon, or GeometryCollection object"
            )

        return v