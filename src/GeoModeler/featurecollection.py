# GeoModeler/src/featurecollection.py
from typing import List, Optional, Annotated, Literal

from pydantic import BaseModel
from pydantic import field_validator, Field, BeforeValidator

from GeoModeler import Feature
from .validators import validate_bbox, type_validator


BBox = Annotated[Optional[List[float]], BeforeValidator(validate_bbox)]


class FeatureCollection(BaseModel, extra='allow'):
    type: Annotated[Literal['FeatureCollection'], Field(default='FeatureCollection', title='Type',
                                                 description='A literal type indicating the GeoJSON object type. '
                                                             'Always "FeatureCollection" for this class.')]
    features: Annotated[List[Feature], Field(None, title='Features', description='A list of features')]
    bbox: BBox = Field(None,
                       title='Bounding Box (bbox)',
                       description="The Bounding Box (bbox) is a list of numbers conforming to values as "
                                   "described in RFC 7946.")

    @field_validator('features')
    @classmethod
    def validate_features(cls, v):
        if not isinstance(v, list):
            raise ValueError("Features must be a list")
        if len(v) > 0:
            for feature in v:
                if not isinstance(feature, Feature):
                    raise ValueError("Features list must contain only Feature objects")
        return v
