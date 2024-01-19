# GeoJSON Models

This project provides a set of Python models for GeoJSON objects conforming to RFC 7946. It includes models for all the basic GeoJSON types:

- Point
- MultiPoint
- LineString
- MultiLineString
- Polygon
- MultiPolygon
- GeometryCollection
- Feature
- FeatureCollection

These models are implemented using the Pydantic library, which provides runtime data validation and settings management using Python type annotations.

## Installation

This project requires Python 3.10 or higher. You can install it using pip:

```bash
pip install geo-modeler
```

## Usage

Here is an example of how to create a Point object:

```python
from src import Point

point = Point(type='Point', coordinates=[1.0, 2.0])
```

You can also validate a GeoJSON string:

```python
point = Point.validate_json('{"type":"Point","coordinates":[1.0,2.0]}')
```

And convert a model to a GeoJSON string:

```python
json_string = point.model_dump_json()
```
### Initializing and Validating
To initialize a `FeatureCollection` or a `Point` using their corresponding JSON representations, you can use the `validate_json` method provided by the `geojson_models` library. This method will take care of all subtypes and validate the structure of the GeoJSON.

If the GeoJSON does not follow the right-hand rule, a warning will be issued, but it won't break the execution. 

When dumping the model to a GeoJSON string using the `model_dump_json` method, you can use the `unset` option to exclude empty defaults.

Here is an example of how to use these features:

```python
from src import FeatureCollection, Point

# Initialize a FeatureCollection with data Point from a JSON string.
feature_collection_json = '{"type":"FeatureCollection","features":[{"type":"Feature","properties":{"id":"1","name":"Litter Bin","description":"Litter Bin","type":"Litter Bin","colour":"Green","location":"Leeds","location_type":"Street","location_subtype":"Road","location_name":"Leeds","latitude":"53.71583","longitude":"-1.74448","easting":"429000","northing":"433000","northing":"433000","postcode_sector":"LS1","postcode_district":"LS","postcode_area":"LS","uprn":"100335","organisation":"Leeds City Council","organisation_uri":"http://opendatacommunities.org/id/leeds-city-council","organisation_label":"Leeds City Council","uri":"http://opendatacommunities.org/id/litter-bin/leeds/1","label":"Litter Bin","notation":"1","notation_uri":"http://opendatacommunities.org/id/litter-bin/leeds/1","notation_label":"1","notation_type":"http://opendatacommunities.org/def/litter-bin/leeds/notation","notation_type_label":"Notation"},"geometry":{"type":"Point","coordinates":[-1.74448,53.71583]}}]}'
feature_collection = FeatureCollection.model_validate_json(feature_collection_json)

# Initialize a single Point with a JSON string
point_json = '{"type":"Point","coordinates":[1.0,2.0]}'
point = Point.model_validate_json(point_json)


# Dump the models to GeoJSON strings, excluding empty defaults
print(feature_collection.model_dump_json(exclude_unset=True))
# {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"id":"1","name":"Litter Bin","description":"Litter Bin","type":"Litter Bin","colour":"Green","location":"Leeds","location_type":"Street","location_subtype":"Road","location_name":"Leeds","latitude":"53.71583","longitude":"-1.74448","easting":"429000","northing":"433000","postcode_sector":"LS1","postcode_district":"LS","postcode_area":"LS","uprn":"100335","organisation":"Leeds City Council","organisation_uri":"http://opendatacommunities.org/id/leeds-city-council","organisation_label":"Leeds City Council","uri":"http://opendatacommunities.org/id/litter-bin/leeds/1","label":"Litter Bin","notation":"1","notation_uri":"http://opendatacommunities.org/id/litter-bin/leeds/1","notation_label":"1","notation_type":"http://opendatacommunities.org/def/litter-bin/leeds/notation","notation_type_label":"Notation"},"geometry":{"type":"Point","coordinates":[-1.74448,53.71583]}}]}
print(point.model_dump_json())
# {"type":"Point","coordinates":[1.0,2.0]}
```

This will output valid GeoJSON, although it may contain warnings for direction. The `model_validate_json` method also validates lengths and required fields according to the GeoJSON specification.
## Testing

This project includes a suite of tests that you can run using pytest:

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.