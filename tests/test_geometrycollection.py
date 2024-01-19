import json

import pytest
from pydantic import ValidationError

from geo_modeler.geometrycollection import GeometryCollection
from geo_modeler.linestring import LineString
from geo_modeler.multilinestring import MultiLineString
from geo_modeler.multipoint import MultiPoint
from geo_modeler.multipolygon import MultiPolygon
from geo_modeler.point import Point
from geo_modeler.polygon import Polygon

valid_geometries = [
    Point(coordinates=[0.0, 0.0]),
    LineString(coordinates=[[0.0, 0.0], [1.0, 1.0]]),
    Polygon(coordinates=[[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]]),
    MultiPoint(coordinates=[[0.0, 0.0], [1.0, 1.0]]),
    MultiLineString(coordinates=[[[0.0, 0.0], [1.0, 1.0]], [[-1.0, -1.0], [-2.0, -2.0]]]),
    MultiPolygon(coordinates=[[[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]]])
]

valid_geometries_json = '{"type":"GeometryCollection","geometries":[{"type":"Point","coordinates":[0.0,0.0]},{"type":"LineString","coordinates":[[0.0,0.0],[1.0,1.0]]},{"type":"Polygon","coordinates":[[[0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0],[0.0,0.0]]]},{"type":"MultiPoint","coordinates":[[0.0,0.0],[1.0,1.0]]},{"type":"MultiLineString","coordinates":[[[0.0,0.0],[1.0,1.0]],[[-1.0,-1.0],[-2.0,-2.0]]]},{"type":"MultiPolygon","coordinates":[[[[0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0],[0.0,0.0]]]]}]}'

valid_model_dump = {
    'type': 'GeometryCollection',
    'geometries': [
        {'type': 'Point', 'coordinates': [0.0, 0.0]},
        {'type': 'LineString', 'coordinates': [[0.0, 0.0], [1.0, 1.0]]},
        {'type': 'Polygon', 'coordinates': [[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]]},
        {'type': 'MultiPoint', 'coordinates': [[0.0, 0.0], [1.0, 1.0]]},
        {'type': 'MultiLineString', 'coordinates': [[[0.0, 0.0], [1.0, 1.0]], [[-1.0, -1.0], [-2.0, -2.0]]]},
        {'type': 'MultiPolygon', 'coordinates': [[[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]]]]}
    ]
}


def test_geometry_collection_with_valid_geometries():
    geometry_collection = GeometryCollection(type='GeometryCollection', geometries=valid_geometries)
    assert geometry_collection.type == 'GeometryCollection'
    assert geometry_collection.geometries == valid_geometries


def test_geometry_collection_with_invalid_type():
    with pytest.raises(ValueError):
        GeometryCollection(type='InvalidType', geometries=[])


def test_geometry_collection_with_invalid_geometries():
    with pytest.raises(ValueError):
        GeometryCollection(type='GeometryCollection', geometries=['InvalidGeometry'])


def test_geometry_collection_with_empty_geometries():
    model = GeometryCollection(type='GeometryCollection', geometries=[])
    assert model.type == 'GeometryCollection'
    assert model.geometries == []



def test_dump_model():
    model = GeometryCollection(type='GeometryCollection', geometries=valid_geometries)
    dumped_model = model.model_dump()
    assert dumped_model == valid_model_dump


def test_dump_model_json():
    model = GeometryCollection(type='GeometryCollection', geometries=valid_geometries)
    dumped_model_json = model.model_dump_json()
    assert dumped_model_json == valid_geometries_json


def test_validate_model():
    # Ensure all objects in the list are valid geometry objects

    # Validate the model
    model = GeometryCollection.model_validate(valid_model_dump)
    assert model.model_dump() == valid_model_dump


def test_validate_model_json():
    model = GeometryCollection.model_validate_json(valid_geometries_json)
    assert model.model_dump() == valid_model_dump


def test_validate_model_json_with_invalid_json():
    with pytest.raises(ValidationError):
        GeometryCollection.model_validate_json('invalid json')

def test_geometry_collection_with_invalid_geometries_using_tuples():
    invalid_geometries = "invalid geometries"
    with pytest.raises(ValueError):
        GeometryCollection(type='GeometryCollection', geometries=invalid_geometries)