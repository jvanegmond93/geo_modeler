# GeoModeler

GeoModeler is a Python project based on Pydantic, designed to model and validate GeoJSON data structures such as points, lines, and polygons. It provides a set of tools and validators for working with GeoJSON data conforming to RFC 7946.

## Features

- Models for all basic GeoJSON types:
  - Point
  - MultiPoint
  - LineString
  - MultiLineString
  - Polygon
  - MultiPolygon
  - GeometryCollection
  - Feature
  - FeatureCollection
- Runtime data validation using Pydantic
- JSON schema generation and validation
- Easy conversion between Python objects and GeoJSON strings

## Installation

GeoModeler requires Python 3.10 or higher. Install it using pip:

```bash
pip install GeoModeler
```

## Usage

### Creating GeoJSON Objects

Here's an example of how to create a `Point` object:

```python
from GeoModeler import Point

point = Point(type='Point', coordinates=[1.0, 2.0])
```

### Validating GeoJSON Strings

You can validate a GeoJSON string using the `model_validate_json` method:

```python
point = Point.model_validate_json('{"type":"Point","coordinates":[1.0,2.0]}')
```

### Converting Models to GeoJSON Strings

Convert a model to a GeoJSON string with the `model_dump_json` method:

```python
json_string = point.model_dump_json()
```

### Initializing and Validating Complex Structures

To initialize a `FeatureCollection` or other complex GeoJSON objects, use the `model_validate_json` method. This ensures that all subtypes are validated correctly:

```python
from GeoModeler import FeatureCollection

feature_collection_json = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"id":"1","name":"Litter Bin","description":"Litter Bin","type":"Litter Bin","colour":"Green","location":"Leeds","latitude":"53.71583","longitude":"-1.74448"},"geometry":{"type":"Point","coordinates":[-1.74448,53.71583]}}]}'
feature_collection = FeatureCollection.model_validate_json(feature_collection_json)
```

### Example with Point

You can also initialize a single `Point` from a JSON string:

```python
from GeoModeler import Point

point_json = '{"type":"Point","coordinates":[1.0,2.0]}'
point = Point.model_validate_json(point_json)
```

### Excluding Unset Values

When dumping models to GeoJSON strings, you can exclude unset defaults:

```python
print(feature_collection.model_dump_json(exclude_unset=True))
print(point.model_dump_json(exclude_unset=True))
```

## Testing

This project includes a suite of tests that can be run using pytest:

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



## Keywords

- geojson
- pydantic
- validation
- geospatial
- data-modeling

## Author

This project is developed and maintained by [jvanegmond](mailto:jvanegmond@silverbirchgeospatial.com).

## Links

- [Homepage](https://github.com/jvanegmond93/geo_modeler)
