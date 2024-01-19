import pytest
from geo_modeler.multilinestring import MultiLineString


def test_multilinestring_initialization_with_three_coordinates_xyz():
    multilinestring = MultiLineString(
        coordinates=[[[1.0, 2.0, 1.0], [3.0, 4.0, 2.0]], [[5.0, 6.0, 3.0], [7.0, 8.0, 4.0]]])
    assert multilinestring.type == 'MultiLineString'
    assert multilinestring.coordinates == [[[1.0, 2.0, 1.0], [3.0, 4.0, 2.0]], [[5.0, 6.0, 3.0], [7.0, 8.0, 4.0]]]


def test_multilinestring_initialization_with_two_coordinates():
    multilinestring = MultiLineString(coordinates=[[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])
    assert multilinestring.type == 'MultiLineString'
    assert multilinestring.coordinates == [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]]


def test_multilinestring_initialization_with_invalid_type():
    with pytest.raises(ValueError):
        MultiLineString(type='invalid', coordinates=[[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])


def test_multilinestring_initialization_with_invalid_coordinates_type():
    with pytest.raises(ValueError):
        MultiLineString(type='MultiLineString', coordinates='invalid')


def test_multilinestring_initialization_with_empty_coordinates():
    with pytest.raises(ValueError):
        MultiLineString(coordinates=[])


def test_multilinestring_initialization_with_one_coordinate():
    with pytest.raises(ValueError):
        MultiLineString(coordinates=[[[1.0, 2.0]]])


def test_multilinestring_initialization_with_more_than_three_coordinates():
    with pytest.raises(ValueError):
        MultiLineString(coordinates=[[[1.0, 2.0, 3.0, 4.0]]])


def test_model_dump_with_valid_multilinestring():
    multilinestring = MultiLineString(type='MultiLineString',
                                      coordinates=[[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])
    assert multilinestring.model_dump() == {'type': 'MultiLineString',
                                            'coordinates': [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]]}


def test_model_dump_json_with_valid_multilinestring():
    multilinestring = MultiLineString(type='MultiLineString',
                                      coordinates=[[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])
    assert multilinestring.model_dump_json() == '{"type":"MultiLineString","coordinates":[[[1.0,2.0],[3.0,4.0]],[[5.0,6.0],[7.0,8.0]]]}'


def test_model_validate_with_valid_dict():
    multilinestring_dict = {'type': 'MultiLineString',
                            'coordinates': [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]]}
    assert MultiLineString.model_validate(multilinestring_dict) == MultiLineString(type='MultiLineString', coordinates=[
        [[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])


def test_model_validate_with_invalid_dict_type():
    with pytest.raises(ValueError):
        MultiLineString.model_validate(
            {'type': 'invalid', 'coordinates': [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]]})


def test_model_validate_with_invalid_dict_coords():
    with pytest.raises(ValueError):
        MultiLineString.model_validate({'type': 'MultiLineString', 'coordinates': [[[1.0, 2.0, 3.0, 4.0]]]})


def test_model_validate_with_invalid_dict():
    with pytest.raises(ValueError):
        MultiLineString.model_validate(
            {'multilinestringType': 'invalid', 'coordinates': [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]]})


def test_model_validate_json_with_valid_geojson():
    geojson = '{"type": "MultiLineString", "coordinates": [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]]}'
    assert MultiLineString.model_validate_json(geojson) == MultiLineString(type='MultiLineString',
                                                                           coordinates=[[[1.0, 2.0], [3.0, 4.0]],
                                                                                        [[5.0, 6.0], [7.0, 8.0]]])


def test_model_validate_json_with_invalid_geojson():
    with pytest.raises(ValueError):
        MultiLineString.model_validate_json(
            '{"type": "invalid", "coordinates": [[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]]}')
