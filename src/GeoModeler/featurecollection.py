# GeoModeler/src/featurecollection.py
from typing import List, Optional, Annotated, Literal
from pydantic import BaseModel, field_validator, Field, BeforeValidator
from .feature import Feature
from .validators import validate_bbox

BBox = Annotated[Optional[List[float]], BeforeValidator(validate_bbox)]

class FeatureCollection(BaseModel, extra='allow'):
    """
    A class used to represent a FeatureCollection in GeoJSON format.

    Attributes
    ----------
    type : Literal['FeatureCollection']
        A literal type indicating the GeoJSON object type. Always 'FeatureCollection' for this class.
    features : List[Feature]
        A list of features. Each feature must be a valid Feature object.
    bbox : Optional[List[float]]
        The bounding box of the feature collection. Must be a valid bounding box as per RFC 7946.

    Methods
    -------
    validate_features(v: List[Feature])
        Validates the 'features' field. Raises a ValueError if the features are not valid.
    model_dump() -> dict
        Returns a dictionary representation of the model.
    model_dump_json() -> str
        Returns a GeoJSON string representation of the model.
    model_validate(v: dict)
        Validates a dictionary representation of the model. Raises a ValueError if the dictionary is not a valid FeatureCollection.

    Examples
    --------
    feature_collection = FeatureCollection(type='FeatureCollection', features=[Feature(id=1, geometry=Point(type='Point', coordinates=[1.0, 2.0]), properties={'name': 'Example'})])
    feature_collection = FeatureCollection(features=[Feature(id=1, geometry=Point(type='Point', coordinates=[1.0, 2.0]), properties={'name': 'Example'})])
    feature_collection = FeatureCollection.model_validate({'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [1.0, 2.0]}, 'properties': {'name': 'Example'}}]})
    feature_collection.model_dump_json() == '{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[1.0,2.0]},"properties":{"name":"Example"}}]}'
    """

    type: Annotated[Literal['FeatureCollection'], Field(default='FeatureCollection', title='Type',
                                                        description='A literal type indicating the GeoJSON object type. '
                                                                    'Always "FeatureCollection" for this class.')]
    features: Annotated[List[Feature], Field(..., title='Features', description='A list of features')]
    bbox: BBox = Field(None,
                       title='Bounding Box (bbox)',
                       description="The Bounding Box (bbox) is a list of numbers conforming to values as "
                                   "described in RFC 7946.")

    @field_validator('features')
    @classmethod
    def validate_features(cls, v):
        """
        Validates the 'features' field.

        This method checks if the features provided are valid. It ensures that 'features' is a list and that each item in the list is a valid Feature object.

        Parameters
        ----------
        v : List[Feature]
            The list of features to validate.

        Returns
        -------
        List[Feature]
            The validated list of features.

        Raises
        ------
        ValueError
            If 'features' is not a list or if any item in the list is not a valid Feature object.
        """
        if not isinstance(v, list):
            raise ValueError("Features must be a list")
        if len(v) > 0:
            for feature in v:
                if not isinstance(feature, Feature):
                    raise ValueError("Features list must contain only Feature objects")
        return v
