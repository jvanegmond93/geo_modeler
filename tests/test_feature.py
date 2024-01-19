import json

import pytest
from src import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection, Feature

def test_feature_creation_with_valid_data():
    feature = Feature(id="123", geometry=Point(coordinates=[0, 0]))
    assert feature.id == "123"
    assert isinstance(feature.geometry, Point)

def test_feature_creation_with_invalid_type():
    with pytest.raises(ValueError):
        Feature(id="123", type="InvalidType", geometry=Point(coordinates=[0, 0]))

def test_feature_creation_with_invalid_geometry():
    with pytest.raises(ValueError):
        Feature(id="123", geometry="InvalidGeometry")

def test_feature_creation_with_number_id():
    feature = Feature(id=123, geometry=Point(coordinates=[0, 0]))
    assert feature.id == 123

def test_feature_creation_with_string_id():
    feature = Feature(id="123", geometry=Point(coordinates=[0, 0]))
    assert feature.id == "123"

def test_feature_dump():
    feature = Feature(id="123", geometry=Point(coordinates=[0, 0]))
    dumped_feature = feature.model_dump()
    assert dumped_feature["id"] == "123"
    assert dumped_feature["geometry"]["coordinates"] == [0, 0]

def test_feature_dump_json():
    feature = Feature(id="123", geometry=Point(coordinates=[0, 0]))
    dumped_feature_json = feature.model_dump_json()
    assert dumped_feature_json == '{"id":"123","type":"Feature","bbox":null,"properties":null,"geometry":{"type":"Point","coordinates":[0.0,0.0]}}'

def test_feature_from_dict():
    feature_dict = {
        "id": "123",
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [0, 0]
        },
        "properties": {}
    }
    feature = Feature.model_validate(feature_dict)
    assert feature.id == "123"
    assert isinstance(feature.geometry, Point)
    assert feature.geometry.coordinates == [0.0, 0.0]

def test_feature_from_json():
    feature_json = '{"id":"123","type":"Feature","geometry":{"type":"Point","coordinates":[0.0,0.0]},"properties":{}}'
    feature = Feature.model_validate_json(feature_json)
    assert feature.id == "123"
    assert isinstance(feature.geometry, Point)
    assert feature.geometry.coordinates == [0.0, 0.0]

def test_feature_from_dict_with_invalid_type():
    feature_dict = {
        "id": "123",
        "type": "InvalidType",
        "geometry": {
            "type": "Point",
            "coordinates": [0, 0]
        },
        "properties": {}
    }
    with pytest.raises(ValueError):
        Feature.model_validate(feature_dict)

def test_feature_from_json_with_invalid_type():
    feature_json = '{"id":"123","type":"InvalidType","geometry":{"type":"Point","coordinates":[0.0,0.0]},"properties":{}}'
    with pytest.raises(ValueError):
        Feature.model_validate_json(feature_json)

def test_feature_from_geojson():
    json_string = """
              {
                  "type": "Feature",
                  "geometry": {
                      "type": "Point",
                      "coordinates": [125.6, 10.1]
                  },
                    "properties": {
                        "name": "Dinagat Islands"
                    }

              }
      """

    feature = Feature.model_validate_json(json_string)

    assert isinstance(feature.geometry, Point)
    assert feature.geometry.coordinates == [125.6, 10.1]
