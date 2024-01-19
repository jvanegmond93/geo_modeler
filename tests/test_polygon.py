# tests/test_polygon.py
import pytest
from geo_modeler.polygon import Polygon


def test_polygon_initialization_with_valid_interior_ring():
    polygon = Polygon(type="Polygon",
                      coordinates=[[[0, 0], [1, 1], [0, 1], [0, 0]], [[0.1, 0.1], [0.1, 0.9], [0.9, 0.9], [0.1, 0.1]]])
    assert polygon.type == "Polygon"
    assert polygon.coordinates == [[[0, 0], [1, 1], [0, 1], [0, 0]], [[0.1, 0.1], [0.1, 0.9], [0.9, 0.9], [0.1, 0.1]]]


def test_polygon_initialization_with_invalid_interior_ring():
    with pytest.raises(ValueError):
        Polygon(type="Polygon",
                coordinates=[[[0, 0], [0, 1], [1, 1], [0, 0]], [[0.1, 0.1], [0.1, 0.9], [0.9, 0.9], [0.9, 0.1]]])


def test_polygon_initialization_with_interior_ring_outside_exterior():

    with pytest.warns(UserWarning):
        Polygon(type="Polygon",
                coordinates=[[[0, 0], [0, 1], [1, 1], [0, 0]], [[-0.1, -0.1], [-0.1, 1.1], [1.1, 1.1], [-0.1, -0.1]]])


def test_polygon_initialization_with_interior_ring_intersecting_exterior():
    with pytest.warns(UserWarning):
        Polygon(type="Polygon",
                coordinates=[[[0, 0], [0, 1], [1, 1], [0, 0]], [[-0.1, 0.5], [0.5, 1.1], [1.1, 0.5], [-0.1, 0.5]]])


def test_polygon_initialization_with_interior_rings_intersecting():
    with pytest.warns(UserWarning):
        Polygon(type="Polygon",
                coordinates=[[[0, 0], [0, 1], [1, 1], [0, 0]], [[0.1, 0.1], [0.1, 0.9], [0.9, 0.9], [0.1, 0.1]],
                             [[0.2, 0.2], [0.2, 0.8], [0.8, 0.8], [0.2, 0.2]]])


def test_polygon_initialization_with_interior_ring_touching_exterior():
    with pytest.warns(UserWarning):
        Polygon(type="Polygon", coordinates=[[[0, 0], [0, 1], [1, 1], [0, 0]], [[0, 0], [0, 0.5], [0.5, 0.5], [0, 0]]])


def test_polygon_initialization_with_interior_rings_touching():
    with pytest.warns(UserWarning):
        Polygon(type="Polygon",
                coordinates=[[[0, 0], [0, 1], [1, 1], [0, 0]], [[0.1, 0.1], [0.1, 0.9], [0.9, 0.9], [0.1, 0.1]],
                             [[0.9, 0.9], [0.9, 1.1], [1.1, 1.1], [0.9, 0.9]]])
