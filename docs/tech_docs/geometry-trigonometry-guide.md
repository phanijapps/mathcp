# Geometry & Trigonometry Documentation

## Overview

The Math Genius library now includes comprehensive geometry and trigonometry functionality, implementing all requirements from Story 2. This documentation provides usage examples and API reference for all geometric operations.

## Quick Start

```python
from mathgenius.api.dispatcher import (
    # Shape calculations
    triangle_area, circle_area, sphere_volume,
    # Trigonometry
    sin, cos, tan, degrees_to_radians,
    # Coordinate geometry
    distance_2d, midpoint_2d, slope,
    # Spatial operations
    vector_add, vector_dot_product, angle_between_vectors
)

# Basic usage examples
area = triangle_area(3, 4)  # 6.0
circumference = circle_circumference(5)  # 31.415...
sin_value = sin(90, 'degrees')  # 1.0
distance = distance_2d((0, 0), (3, 4))  # 5.0
```

## Shape Calculations

### 2D Shapes

#### Triangle Functions

```python
# Area calculation (base × height)
area = triangle_area(5, 8)  # 20.0

# Area using Heron's formula
area = triangle_area_heron(3, 4, 5)  # 6.0

# Perimeter calculation
perimeter = triangle_perimeter(3, 4, 5)  # 12
```

#### Circle Functions

```python
# Area calculation
area = circle_area(3)  # 28.274...

# Circumference calculation
circumference = circle_circumference(3)  # 18.849...
```

#### Rectangle Functions

```python
# Area calculation
area = rectangle_area(4, 6)  # 24

# Perimeter calculation
perimeter = rectangle_perimeter(4, 6)  # 20
```

#### Polygon Functions

```python
# Area using shoelace formula
square_coords = [(0, 0), (2, 0), (2, 2), (0, 2)]
area = polygon_area(square_coords)  # 4.0

# Perimeter calculation
perimeter = polygon_perimeter(square_coords)  # 8.0
```

### 3D Shapes

#### Sphere Functions

```python
# Volume calculation
volume = sphere_volume(3)  # 113.097...

# Surface area calculation
surface_area = sphere_surface_area(3)  # 113.097...
```

#### Cylinder Functions

```python
# Volume calculation
volume = cylinder_volume(2, 5)  # 62.831...

# Surface area calculation
surface_area = cylinder_surface_area(2, 5)  # 87.964...
```

#### Cube Functions

```python
# Volume calculation
volume = cube_volume(3)  # 27

# Surface area calculation
surface_area = cube_surface_area(3)  # 54
```

#### Pyramid Functions

```python
# Volume calculation
volume = pyramid_volume(12, 8)  # 32.0

# Surface area calculation
surface_area = pyramid_surface_area(16, 16, 5)  # 56.0
```

## Trigonometry

### Basic Trigonometric Functions

```python
import math

# Sine function
sin_rad = sin(math.pi/2)  # 1.0
sin_deg = sin(90, 'degrees')  # 1.0

# Cosine function
cos_rad = cos(0)  # 1.0
cos_deg = cos(0, 'degrees')  # 1.0

# Tangent function
tan_rad = tan(math.pi/4)  # 1.0
tan_deg = tan(45, 'degrees')  # 1.0
```

### Inverse Trigonometric Functions

```python
# Arcsine
angle_rad = asin(0.5)  # π/6 radians
angle_deg = asin(0.5, 'degrees')  # 30 degrees

# Arccosine
angle_rad = acos(0.5)  # π/3 radians
angle_deg = acos(0.5, 'degrees')  # 60 degrees

# Arctangent
angle_rad = atan(1)  # π/4 radians
angle_deg = atan(1, 'degrees')  # 45 degrees
```

### Hyperbolic Functions

```python
# Hyperbolic sine
sinh_val = sinh(1)  # 1.175...

# Hyperbolic cosine
cosh_val = cosh(1)  # 1.543...

# Hyperbolic tangent
tanh_val = tanh(1)  # 0.761...
```

### Angle Conversion

```python
# Convert degrees to radians
radians = degrees_to_radians(180)  # π

# Convert radians to degrees
degrees = radians_to_degrees(math.pi)  # 180
```

## Coordinate Geometry

### Distance Calculations

```python
# 2D distance
distance = distance_2d((0, 0), (3, 4))  # 5.0

# 3D distance
distance = distance_3d((0, 0, 0), (3, 4, 12))  # 13.0
```

### Midpoint Calculations

```python
# 2D midpoint
midpoint = midpoint_2d((0, 0), (4, 6))  # (2.0, 3.0)

# 3D midpoint
midpoint = midpoint_3d((0, 0, 0), (6, 8, 10))  # (3.0, 4.0, 5.0)
```

### Line Operations

```python
# Calculate slope
slope_value = slope((0, 0), (2, 4))  # 2.0

# Get line equation
equation = line_equation((0, 0), (1, 2))
# {'type': 'linear', 'slope': 2.0, 'intercept': 0.0}

# Find line intersection
intersection = line_intersection((0, 0), (2, 2), (0, 2), (2, 0))
# (1.0, 1.0)

# Point to line distance
distance = point_to_line_distance((0, 0), (1, 1), (2, 0))  # 1.414...
```

## Spatial Operations

### Vector Operations

```python
# Vector addition
result = vector_add((1, 2), (3, 4))  # (4, 6)

# Vector subtraction
result = vector_subtract((5, 7), (2, 3))  # (3, 4)

# Dot product
dot_product = vector_dot_product((1, 2), (3, 4))  # 11

# Cross product (3D only)
cross_product = vector_cross_product((1, 0, 0), (0, 1, 0))  # (0, 0, 1)

# Vector magnitude
magnitude = vector_magnitude((3, 4))  # 5.0

# Vector normalization
unit_vector = vector_normalize((3, 4))  # (0.6, 0.8)
```

### Angle Calculations

```python
# Angle between vectors
angle_rad = angle_between_vectors((1, 0), (0, 1))  # π/2 radians
angle_deg = angle_between_vectors((1, 0), (0, 1), 'degrees')  # 90 degrees
```

### Geometric Transformations

```python
# Rotate point
rotated = rotate_point((1, 0), 90, unit='degrees')  # (0.0, 1.0)

# Translate point
translated = translate_point((1, 2), (3, 4))  # (4, 6)

# Scale point
scaled = scale_point((2, 4), 2)  # (4, 8)
```

## Error Handling

All geometry functions use consistent error handling:

```python
from mathgenius.core.errors import ValidationError, CalculationError

try:
    # Invalid input
    triangle_area("invalid", 4)
except ValidationError as e:
    print(f"Validation error: {e}")

try:
    # Mathematical error
    tan(90, 'degrees')  # Undefined
except CalculationError as e:
    print(f"Calculation error: {e}")
```

## Complex Examples

### Calculate Triangle Properties

```python
# Given three vertices of a triangle
p1 = (0, 0)
p2 = (3, 0)
p3 = (0, 4)

# Calculate side lengths
side1 = distance_2d(p1, p2)  # 3.0
side2 = distance_2d(p2, p3)  # 5.0
side3 = distance_2d(p3, p1)  # 4.0

# Calculate area using Heron's formula
area = triangle_area_heron(side1, side2, side3)  # 6.0

# Calculate perimeter
perimeter = triangle_perimeter(side1, side2, side3)  # 12.0
```

### Vector Analysis

```python
# Create vectors from points
start = (1, 2)
end = (4, 6)

# Calculate vector
vector = vector_subtract(end, start)  # (3, 4)

# Get magnitude and direction
magnitude = vector_magnitude(vector)  # 5.0
unit_vector = vector_normalize(vector)  # (0.6, 0.8)

# Calculate angle from x-axis
angle = angle_between_vectors(vector, (1, 0), 'degrees')  # 53.13...
```

### Geometric Transformation Chain

```python
# Start with a point
point = (1, 0)

# Apply transformations
translated = translate_point(point, (2, 3))  # (3, 3)
rotated = rotate_point(translated, 45, unit='degrees')  # (0, 4.24...)
scaled = scale_point(rotated, 2)  # (0, 8.48...)
```

## API Reference

All geometry functions are available through the unified API:

```python
from mathgenius.api.dispatcher import *

# Or import specific modules
from mathgenius.geometry import shapes, trigonometry, coordinates, spatial
```

For detailed function signatures and parameters, refer to the individual module documentation or use Python's built-in help system:

```python
help(triangle_area)
help(sin)
help(distance_2d)
help(vector_add)
```
