import pytest
from src.point import Point


def test_point_initialization_with_valid_coordinates_and_type():
    point = Point(coordinates=[1.0, 2.0, 3.0])
    assert point.type == 'Point'
    assert point.coordinates == [1.0, 2.0, 3.0]


def test_point_initialization_with_two_coordinates():
    point = Point(coordinates=[1.0, 2.0])
    assert point.type == 'Point'
    assert point.coordinates == [1.0, 2.0]


def test_point_initialization_with_invalid_type():
    with pytest.raises(ValueError):
        Point(type='invalid', coordinates=[1.0, 2.0, 3.0])


def test_point_initialization_with_invalid_coordinates_type():
    with pytest.raises(ValueError):
        Point(type='Point', coordinates='invalid')


def test_point_initialization_with_empty_coordinates():
    with pytest.raises(ValueError):
        Point( coordinates=[])


def test_point_initialization_with_one_coordinate():
    with pytest.raises(ValueError):
        Point(type='Point', coordinates=[])


def test_point_initialization_with_more_than_three_coordinates():
    with pytest.raises(ValueError):
        Point(type='Point', coordinates=[1.0, 2.0, 3.0, 4.0])


def test_model_dump_with_valid_point():
    point = Point(type='Point', coordinates=[1.0, 2.0, 3.0])
    assert point.model_dump() == {'type': 'Point', 'coordinates': [1.0, 2.0, 3.0]}


def test_model_dump_with_valid_point():
    point = Point(type='Point', coordinates=[1.0, 2.0, 3.0])
    assert point.model_dump() == {'type': 'Point', 'coordinates': [1.0, 2.0, 3.0]}


def test_model_dump_json_with_valid_point():
    point = Point(type='Point', coordinates=[1.0, 2.0, 3.0])
    assert point.model_dump_json() == '{"type":"Point","coordinates":[1.0,2.0,3.0]}'


def test_model_validate_with_valid_dict():
    point_dict = {'type': 'Point', 'coordinates': [1.0, 2.0, 3.0]}
    assert Point.model_validate(point_dict) == Point(type='Point', coordinates=[1.0, 2.0, 3.0])


def test_model_validate_with_invalid_dict_type():
    with pytest.raises(ValueError):
        Point.model_validate({'type': 'invalid', 'coordinates': [1.0, 2.0, 3.0]})


def test_model_validate_with_invalid_dict_coords():
    with pytest.raises(ValueError):
        Point.model_validate({'type': 'Point', 'coordinates': [1.0, 2.0, 3.0, 4.0]})


def test_model_validate_with_invalid_dict():
    with pytest.raises(ValueError):
        Point.model_validate({'pointType': 'invalid', 'coordinates': [1.0, 2.0, 3.0]})


def test_model_validate_json_with_valid_geojson():
    geojson = '{"type": "Point", "coordinates": [1.0, 2.0, 3.0]}'
    assert Point.model_validate_json(geojson) == Point(type='Point', coordinates=[1.0, 2.0, 3.0])


def test_model_validate_json_with_invalid_geojson():
    with pytest.raises(ValueError):
        Point.model_validate_json('{"type": "invalid", "coordinates": [1.0, 2.0, 3.0]}')
