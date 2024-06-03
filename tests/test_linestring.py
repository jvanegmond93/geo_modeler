import pytest
from pydantic import ValidationError

from GeoModeler import LineString


def test_linestring_initialization_with_valid_coordinates_and_type():
    linestring = LineString(coordinates=[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]])
    assert linestring.type == 'LineString'
    assert linestring.coordinates == [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]]


def test_linestring_initialization_with_two_coordinates():
    linestring = LineString(coordinates=[[1.0, 2.0], [3.0, 4.0]])
    assert linestring.type == 'LineString'
    assert linestring.coordinates == [[1.0, 2.0], [3.0, 4.0]]


def test_linestring_initialization_with_invalid_type():
    with pytest.raises(ValueError):
        LineString(type='invalid', coordinates=[[1.0, 2.0], [3.0, 4.0]])


def test_linestring_initialization_with_invalid_coordinates_type():
    with pytest.raises(ValidationError):
        LineString(type='LineString', coordinates='invalid')


def test_linestring_initialization_with_empty_coordinates():
    with pytest.raises(ValueError):
        LineString(coordinates=[])


def test_linestring_initialization_with_one_coordinate():
    with pytest.raises(ValueError):
        LineString(coordinates=[[1.0, 2.0]])


def test_linestring_initialization_with_more_than_three_coordinates():
    with pytest.raises(ValueError):
        LineString(coordinates=[[1.0, 2.0, 3.0, 4.0]])


def test_model_dump_with_valid_linestring():
    linestring = LineString(type='LineString', coordinates=[[1.0, 2.0], [3.0, 4.0]])
    assert linestring.model_dump() == {'type': 'LineString', 'coordinates': [[1.0, 2.0], [3.0, 4.0]]}


def test_model_dump_json_with_valid_linestring():
    linestring = LineString(type='LineString', coordinates=[[1.0, 2.0], [3.0, 4.0]])
    assert linestring.model_dump_json() == '{"type":"LineString","coordinates":[[1.0,2.0],[3.0,4.0]]}'


def test_model_validate_with_valid_dict():
    linestring_dict = {'type': 'LineString', 'coordinates': [[1.0, 2.0], [3.0, 4.0]]}
    assert LineString.model_validate(linestring_dict) == LineString(type='LineString',
                                                                    coordinates=[[1.0, 2.0], [3.0, 4.0]])


def test_model_validate_with_invalid_dict_type():
    with pytest.raises(ValueError):
        LineString.model_validate({'type': 'invalid', 'coordinates': [[1.0, 2.0], [3.0, 4.0]]})


def test_model_validate_with_invalid_dict_coords():
    with pytest.raises(ValueError):
        LineString.model_validate({'type': 'LineString', 'coordinates': [[1.0, 2.0, 3.0, 4.0]]})


def test_model_validate_with_invalid_dict():
    with pytest.raises(ValueError):
        LineString.model_validate({'linestringType': 'invalid', 'coordinates': [[1.0, 2.0], [3.0, 4.0]]})


def test_model_validate_json_with_valid_geojson():
    geojson = '{"type": "LineString", "coordinates": [[1.0, 2.0], [3.0, 4.0]]}'
    assert LineString.model_validate_json(geojson) == LineString(type='LineString',
                                                                 coordinates=[[1.0, 2.0], [3.0, 4.0]])


def test_model_validate_json_with_invalid_geojson():
    with pytest.raises(ValueError):
        LineString.model_validate_json('{"type": "invalid", "coordinates": [[1.0, 2.0], [3.0, 4.0]]}')
