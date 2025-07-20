"""Geometric shapes calculations for mathgenius."""

import math
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError

def validate_positive_number(value, name="value"):
    """Validate that a value is a positive number."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"Invalid input: {name} must be a number.")
    if value <= 0:
        raise ValueError(f"Invalid input: {name} must be positive.")
    return value

def validate_non_negative_number(value, name="value"):
    """Validate that a value is a non-negative number."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"Invalid input: {name} must be a number.")
    if value < 0:
        raise ValueError(f"Invalid input: {name} must be non-negative.")
    return value

def validate_coordinate_list(coordinates, min_length=3, name="coordinates"):
    """Validate a list of coordinates."""
    if not isinstance(coordinates, (list, tuple)):
        raise ValueError(f"Invalid input: {name} must be a list or tuple.")
    if len(coordinates) < min_length:
        raise ValueError(f"Invalid input: {name} must have at least {min_length} points.")
    for i, coord in enumerate(coordinates):
        if not isinstance(coord, (list, tuple)) or len(coord) != 2:
            raise ValueError(f"Invalid input: {name}[{i}] must be a 2D coordinate (x, y).")
        validate_numbers(coord[0], coord[1])
    return coordinates

# 2D Shape Area Calculations

def triangle_area(base, height):
    """Calculate the area of a triangle given base and height."""
    try:
        validate_positive_number(base, "base")
        validate_positive_number(height, "height")
        return 0.5 * base * height
    except ValueError as e:
        raise ValidationError(str(e))

def triangle_area_heron(a, b, c):
    """Calculate the area of a triangle using Heron's formula."""
    try:
        validate_positive_number(a, "side a")
        validate_positive_number(b, "side b")
        validate_positive_number(c, "side c")
        
        # Check triangle inequality
        if a + b <= c or a + c <= b or b + c <= a:
            raise CalculationError("Invalid triangle: sides do not satisfy triangle inequality.")
        
        s = (a + b + c) / 2  # semi-perimeter
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))
        return area
    except ValueError as e:
        raise ValidationError(str(e))

def circle_area(radius):
    """Calculate the area of a circle."""
    try:
        validate_positive_number(radius, "radius")
        return math.pi * radius ** 2
    except ValueError as e:
        raise ValidationError(str(e))

def rectangle_area(length, width):
    """Calculate the area of a rectangle."""
    try:
        validate_positive_number(length, "length")
        validate_positive_number(width, "width")
        return length * width
    except ValueError as e:
        raise ValidationError(str(e))

def polygon_area(coordinates):
    """Calculate the area of a polygon using the shoelace formula."""
    try:
        validate_coordinate_list(coordinates, min_length=3, name="coordinates")
        
        n = len(coordinates)
        area = 0
        for i in range(n):
            j = (i + 1) % n
            area += coordinates[i][0] * coordinates[j][1]
            area -= coordinates[j][0] * coordinates[i][1]
        
        return abs(area) / 2
    except ValueError as e:
        raise ValidationError(str(e))

# 2D Shape Perimeter Calculations

def triangle_perimeter(a, b, c):
    """Calculate the perimeter of a triangle."""
    try:
        validate_positive_number(a, "side a")
        validate_positive_number(b, "side b")
        validate_positive_number(c, "side c")
        
        # Check triangle inequality
        if a + b <= c or a + c <= b or b + c <= a:
            raise CalculationError("Invalid triangle: sides do not satisfy triangle inequality.")
        
        return a + b + c
    except ValueError as e:
        raise ValidationError(str(e))

def circle_circumference(radius):
    """Calculate the circumference of a circle."""
    try:
        validate_positive_number(radius, "radius")
        return 2 * math.pi * radius
    except ValueError as e:
        raise ValidationError(str(e))

def rectangle_perimeter(length, width):
    """Calculate the perimeter of a rectangle."""
    try:
        validate_positive_number(length, "length")
        validate_positive_number(width, "width")
        return 2 * (length + width)
    except ValueError as e:
        raise ValidationError(str(e))

def polygon_perimeter(coordinates):
    """Calculate the perimeter of a polygon."""
    try:
        validate_coordinate_list(coordinates, min_length=3, name="coordinates")
        
        perimeter = 0
        n = len(coordinates)
        for i in range(n):
            j = (i + 1) % n
            dx = coordinates[j][0] - coordinates[i][0]
            dy = coordinates[j][1] - coordinates[i][1]
            perimeter += math.sqrt(dx ** 2 + dy ** 2)
        
        return perimeter
    except ValueError as e:
        raise ValidationError(str(e))

# 3D Shape Volume Calculations

def sphere_volume(radius):
    """Calculate the volume of a sphere."""
    try:
        validate_positive_number(radius, "radius")
        return (4/3) * math.pi * radius ** 3
    except ValueError as e:
        raise ValidationError(str(e))

def cylinder_volume(radius, height):
    """Calculate the volume of a cylinder."""
    try:
        validate_positive_number(radius, "radius")
        validate_positive_number(height, "height")
        return math.pi * radius ** 2 * height
    except ValueError as e:
        raise ValidationError(str(e))

def cube_volume(side):
    """Calculate the volume of a cube."""
    try:
        validate_positive_number(side, "side")
        return side ** 3
    except ValueError as e:
        raise ValidationError(str(e))

def pyramid_volume(base_area, height):
    """Calculate the volume of a pyramid."""
    try:
        validate_positive_number(base_area, "base_area")
        validate_positive_number(height, "height")
        return (1/3) * base_area * height
    except ValueError as e:
        raise ValidationError(str(e))

# 3D Shape Surface Area Calculations

def sphere_surface_area(radius):
    """Calculate the surface area of a sphere."""
    try:
        validate_positive_number(radius, "radius")
        return 4 * math.pi * radius ** 2
    except ValueError as e:
        raise ValidationError(str(e))

def cylinder_surface_area(radius, height):
    """Calculate the surface area of a cylinder."""
    try:
        validate_positive_number(radius, "radius")
        validate_positive_number(height, "height")
        return 2 * math.pi * radius * (radius + height)
    except ValueError as e:
        raise ValidationError(str(e))

def cube_surface_area(side):
    """Calculate the surface area of a cube."""
    try:
        validate_positive_number(side, "side")
        return 6 * side ** 2
    except ValueError as e:
        raise ValidationError(str(e))

def pyramid_surface_area(base_area, base_perimeter, slant_height):
    """Calculate the surface area of a pyramid."""
    try:
        validate_positive_number(base_area, "base_area")
        validate_positive_number(base_perimeter, "base_perimeter")
        validate_positive_number(slant_height, "slant_height")
        return base_area + (0.5 * base_perimeter * slant_height)
    except ValueError as e:
        raise ValidationError(str(e))
