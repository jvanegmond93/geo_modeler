import pytest

from geo_modeler.multipolygon import MultiPolygon


def test_valid_multipolygon_creation():
    multipolygon = MultiPolygon(type='MultiPolygon', coordinates=[
        [
            [
                [102.0, 2.0],
                [103.0, 2.0],
                [103.0, 3.0],
                [102.0, 3.0],
                [102.0, 2.0]
            ]
        ],
        [
            [
                [100.0, 0.0],
                [101.0, 0.0],
                [101.0, 1.0],
                [100.0, 1.0],
                [100.0, 0.0]
            ],
            [
                [100.2, 0.2],
                [100.2, 0.8],
                [100.8, 0.8],
                [100.8, 0.2],
                [100.2, 0.2]
            ]
        ]
    ])

    assert multipolygon.type == 'MultiPolygon'
    assert multipolygon.coordinates == [
        [
            [
                [102.0, 2.0],
                [103.0, 2.0],
                [103.0, 3.0],
                [102.0, 3.0],
                [102.0, 2.0]
            ]
        ],
        [
            [
                [100.0, 0.0],
                [101.0, 0.0],
                [101.0, 1.0],
                [100.0, 1.0],
                [100.0, 0.0]
            ],
            [
                [100.2, 0.2],
                [100.2, 0.8],
                [100.8, 0.8],
                [100.8, 0.2],
                [100.2, 0.2]
            ]
        ]
    ]


valid_test_2 = {'coordinates': [[[[0.0, 0.0],
                                  [1.0, 0.0],
                                  [1.0, 1.0],
                                  [0.0, 1.0],
                                  [0.0, 0.0]]]],
                'type': 'MultiPolygon'}


def test_polygon_invalid_type_multipolygon_creation():
    with pytest.raises(ValueError):
        MultiPolygon(type='Polygon', coordinates=[[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]])


def test_polygon_invalid_coordinates_multipolygon_creation():
    with pytest.raises(ValueError):
        MultiPolygon(type='MultiPolygon', coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]])


def test_polygon_invalid_polygon_in_multipolygon_creation():
    with pytest.raises(ValueError):
        MultiPolygon(type='MultiPolygon', coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]], [[1.0, 2.0]]])


def test_polygon_invalid_linear_ring_in_multipolygon_creation():
    with pytest.raises(ValueError):
        MultiPolygon(type='MultiPolygon',
                     coordinates=[[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]], [[1.0, 2.0], [3.0, 4.0]]]])


def test_multipolygon_creation_with_empty_coordinates():
    with pytest.raises(ValueError):
        MultiPolygon(type='MultiPolygon', coordinates=[])


def test_multipolygon_creation_with_improperly_nested_coordinates():
    with pytest.raises(ValueError):
        MultiPolygon(type='MultiPolygon', coordinates=[1.0, 2.0])


def test_multipolygon_creation_with_non_matching_first_and_last_coordinates():
    with pytest.raises(ValueError):
        MultiPolygon(type='MultiPolygon', coordinates=[[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [7.0, 8.0]]]])
