# GeoModeler/src/feature.py
from typing import Annotated, Any, Dict, Union, Optional, List, Literal
from pydantic import BaseModel, field_validator, Field, ConfigDict, BeforeValidator, AfterValidator
from .point import Point
from .validators import validate_bbox, type_validator

class Feature(BaseModel, extra='allow'):
    """
    A class used to represent a Feature in GeoJSON format.

    Attributes
    ----------
    id : Optional[Union[str, int]]
        The ID of the feature.
    type : Literal['Feature']
        A literal type indicating the GeoJSON object type. Always 'Feature' for this class.
    bbox : Optional[List[float]]
        The bounding box of the feature. Must be a valid bounding box as per RFC 7946.
    properties : Optional[Dict[str, Any]]
        The properties of the feature.
    geometry : Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection]
        The geometry of the feature.

    Methods
    -------
    validate_type(v: str)
        Validates the 'type' field. Raises a ValueError if the type is not 'Feature'.

    model_dump() -> dict
        Returns a dictionary representation of the model.
    model_dump_json() -> str
        Returns a GeoJSON string representation of the model.

    validate_geometry(v: Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection])
        Validates the 'geometry' field. Raises a ValueError if the geometry is not a valid GeoJSON geometry.

    model_validate(v: dict)
        Validates a dictionary representation of the model. Raises a ValueError if the dictionary is not a valid Feature.

    Examples
    --------
    feature = Feature(id=1, geometry=Point(type='Point', coordinates=[1.0, 2.0]), properties={'name': 'Example'})
    feature = Feature(geometry=Point(type='Point', coordinates=[1.0, 2.0]))
    feature = Feature.model_validate({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [1.0, 2.0]}, 'properties': {'name': 'Example'}})
    feature.model_dump_json() == '{"type":"Feature","geometry":{"type":"Point","coordinates":[1.0,2.0]},"properties":{"name":"Example"}}'
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    id: Annotated[Optional[Union[str, int]], Field(None, title='ID', description='The ID of the feature')]
    type: Literal['Feature'] = Field(default='Feature', title='Type',
                                     description='A literal type indicating the GeoJSON object type. '
                                                 'Always "Feature" for this class.')
    bbox: Annotated[Optional[List[float]], Field(None,
                                                 title='Bounding Box (bbox)',
                                                 description="The Bounding Box (bbox) is a list of numbers conforming to values as "
                                                             "described in RFC 7946.")]
    properties: Annotated[Optional[Dict[str, Any]], Field(None, title='Properties')]
    geometry: Annotated[
        Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection],
        Field(..., title='Geometry', discriminator='type')
    ]

    @field_validator('geometry', mode='after')
    def validate_geometry(cls, v: Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection]):
        """
        Validates the 'geometry' field.

        This method checks if the geometry provided is valid. It ensures that the geometry is an instance of one of the valid GeoJSON geometry types.

        Parameters
        ----------
        v : Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection]
            The geometry to validate.

        Returns
        -------
        Union[Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection]
            The validated geometry.

        Raises
        ------
        ValueError
            If the geometry is not an instance of a valid GeoJSON geometry type.
        """
        if not isinstance(v, (Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection)):
            raise ValueError("Geometry must be a Point, MultiPoint, LineString, MultiLineString, Polygon, "
                             "MultiPolygon, or GeometryCollection object")
        return v
