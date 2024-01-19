from enum import Enum
from typing import List, Tuple, Optional

# A single point in 2D or 3D space
Coordinate = Tuple[float, float, Optional[float]]  # (longitude, latitude, [elevation])

# A line as a series of points
Line = List[Coordinate]

# A polygon as a series of lines
Polygon = List[Line]
BoundingBox = List[float]  # Type alias for a bounding box

