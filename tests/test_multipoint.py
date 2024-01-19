import pytest

from src import MultiPoint


def test_multipoint_initialization_with_valid_coordinates_and_type():
    multipoint = MultiPoint(coordinates=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert multipoint.type == 'MultiPoint'
    assert multipoint.coordinates == [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]


def test_multipoint_initialization_with_two_coordinates():
    multipoint = MultiPoint(coordinates=[[1.0, 2.0], [3.0, 4.0]])
    assert multipoint.type == 'MultiPoint'
    assert multipoint.coordinates == [[1.0, 2.0], [3.0, 4.0]]


def test_multipoint_initialization_with_invalid_type():
    with pytest.raises(ValueError):
        MultiPoint(type='invalid', coordinates=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])


def test_multipoint_initialization_with_invalid_coordinates_type():
    with pytest.raises(ValueError):
        MultiPoint(type='MultiPoint', coordinates='invalid')


def test_multipoint_initialization_with_empty_coordinates():
    with pytest.raises(ValueError):
        MultiPoint(type='MultiPoint', coordinates=[])


def test_multipoint_initialization_with_one_coordinate():
    with pytest.raises(ValueError):
        MultiPoint(type='MultiPoint', coordinates=[[1.0]])


def test_multipoint_initialization_with_more_than_three_coordinates():
    with pytest.raises(ValueError):
        MultiPoint(type='MultiPoint', coordinates=[[1.0, 2.0, 3.0, 4.0]])


def test_model_dump_with_valid_multipoint():
    multipoint = MultiPoint(type='MultiPoint', coordinates=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert multipoint.model_dump() == {'type': 'MultiPoint', 'coordinates': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}


def test_model_dump_json_with_valid_multipoint():
    multipoint = MultiPoint(type='MultiPoint', coordinates=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    assert multipoint.model_dump_json() == '{"type":"MultiPoint","coordinates":[[1.0,2.0,3.0],[4.0,5.0,6.0]]}'


def test_model_validate_with_valid_dict():
    multipoint_dict = {'type': 'MultiPoint', 'coordinates': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}
    assert MultiPoint.model_validate(multipoint_dict) == MultiPoint(type='MultiPoint',
                                                                    coordinates=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])


def test_model_validate_with_invalid_dict_type():
    with pytest.raises(ValueError):
        MultiPoint.model_validate({'type': 'invalid', 'coordinates': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]})


def test_model_validate_with_invalid_dict_coords():
    with pytest.raises(ValueError):
        MultiPoint.model_validate({'type': 'MultiPoint', 'coordinates': [[1.0, 2.0, 3.0, 4.0]]})


def test_model_validate_with_invalid_dict():
    with pytest.raises(ValueError):
        MultiPoint.model_validate({'pointType': 'invalid', 'coordinates': [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]})


def test_model_validate_json_with_valid_geojson():
    geojson = '{"type": "MultiPoint", "coordinates": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}'
    assert MultiPoint.model_validate_json(geojson) == MultiPoint(type='MultiPoint',
                                                                 coordinates=[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])


def test_model_validate_json_with_invalid_geojson():
    with pytest.raises(ValueError):
        MultiPoint.model_validate_json('{"type": "invalid", "coordinates": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}')
