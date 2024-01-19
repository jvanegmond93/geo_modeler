import pytest
from src.featurecollection import FeatureCollection
from src.feature import Feature


def test_feature_collection_with_valid_data():
    feature = Feature(type="Feature", geometry={"type": "Point", "coordinates": [125.6, 10.1]}, properties={})
    feature_collection = FeatureCollection(type="FeatureCollection", features=[feature])
    assert feature_collection.type == "FeatureCollection"
    assert len(feature_collection.features) == 1
    assert isinstance(feature_collection.features[0], Feature)


def test_feature_collection_with_invalid_type():
    with pytest.raises(ValueError):
        FeatureCollection(type="InvalidType", features=[])


def test_feature_collection_with_invalid_features():
    with pytest.raises(ValueError):
        FeatureCollection(type="FeatureCollection", features=["InvalidFeature"])


def test_feature_collection_with_valid_bbox_2d():
    feature = Feature(type="Feature", geometry={"type": "Point", "coordinates": [125.6, 10.1]})
    feature_collection = FeatureCollection(type="FeatureCollection", features=[feature], bbox=[0.0, 0.0, 10.0, 10.0])
    assert feature_collection.bbox == [0.0, 0.0, 10.0, 10.0]


def test_feature_collection_with_valid_bbox_3d():
    feature = Feature(type="Feature", geometry={"type": "Point", "coordinates": [125.6, 10.1]}, properties={})
    feature_collection = FeatureCollection(type="FeatureCollection", features=[feature],
                                           bbox=[0.0, 0.0, 0.0, 10.0, 10.0, 10.0])
    assert feature_collection.bbox == [0.0, 0.0, 0.0, 10.0, 10.0, 10.0]


def test_feature_collection_with_invalid_bbox():
    with pytest.raises(ValueError):
        FeatureCollection(type="FeatureCollection", features=[], bbox=[0.0, 0.0, 10.0])


def test_feature_collection_from_json():
    json_string = """
    {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [125.6, 10.1]
                }

            }
        ]
    }
    """
    feature_collection = FeatureCollection.model_validate_json(json_string)
    assert feature_collection.type == "FeatureCollection"
    assert len(feature_collection.features) == 1
    assert isinstance(feature_collection.features[0], Feature)
    assert feature_collection.features[0].geometry.coordinates == [125.6, 10.1]
