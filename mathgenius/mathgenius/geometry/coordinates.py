"""Coordinate geometry functions for mathgenius."""

import math
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError

def validate_2d_point(point, name="point"):
    """Validate a 2D point (x, y)."""
    if not isinstance(point, (list, tuple)) or len(point) != 2:
        raise ValueError(f"Invalid input: {name} must be a 2D coordinate (x, y).")
    validate_numbers(point[0], point[1])
    return point

def validate_3d_point(point, name="point"):
    """Validate a 3D point (x, y, z)."""
    if not isinstance(point, (list, tuple)) or len(point) != 3:
        raise ValueError(f"Invalid input: {name} must be a 3D coordinate (x, y, z).")
    validate_numbers(point[0], point[1], point[2])
    return point

def validate_line_2d(point1, point2, name1="point1", name2="point2"):
    """Validate two 2D points that define a line."""
    validate_2d_point(point1, name1)
    validate_2d_point(point2, name2)
    
    if point1[0] == point2[0] and point1[1] == point2[1]:
        raise ValueError(f"Invalid input: {name1} and {name2} cannot be the same point.")
    
    return point1, point2

# Distance Calculations

def distance_2d(point1, point2):
    """Calculate the Euclidean distance between two 2D points."""
    try:
        validate_2d_point(point1, "point1")
        validate_2d_point(point2, "point2")
        
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        return math.sqrt(dx**2 + dy**2)
    except ValueError as e:
        raise ValidationError(str(e))

def distance_3d(point1, point2):
    """Calculate the Euclidean distance between two 3D points."""
    try:
        validate_3d_point(point1, "point1")
        validate_3d_point(point2, "point2")
        
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        dz = point2[2] - point1[2]
        return math.sqrt(dx**2 + dy**2 + dz**2)
    except ValueError as e:
        raise ValidationError(str(e))

# Midpoint Calculations

def midpoint_2d(point1, point2):
    """Calculate the midpoint between two 2D points."""
    try:
        validate_2d_point(point1, "point1")
        validate_2d_point(point2, "point2")
        
        mid_x = (point1[0] + point2[0]) / 2
        mid_y = (point1[1] + point2[1]) / 2
        return (mid_x, mid_y)
    except ValueError as e:
        raise ValidationError(str(e))

def midpoint_3d(point1, point2):
    """Calculate the midpoint between two 3D points."""
    try:
        validate_3d_point(point1, "point1")
        validate_3d_point(point2, "point2")
        
        mid_x = (point1[0] + point2[0]) / 2
        mid_y = (point1[1] + point2[1]) / 2
        mid_z = (point1[2] + point2[2]) / 2
        return (mid_x, mid_y, mid_z)
    except ValueError as e:
        raise ValidationError(str(e))

# Slope and Line Calculations

def slope(point1, point2):
    """Calculate the slope of a line between two 2D points."""
    try:
        validate_line_2d(point1, point2)
        
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        
        if dx == 0:
            raise CalculationError("Slope is undefined for vertical lines.")
        
        return dy / dx
    except ValueError as e:
        raise ValidationError(str(e))

def line_equation(point1, point2):
    """Calculate the equation of a line in the form y = mx + b."""
    try:
        validate_line_2d(point1, point2)
        
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        
        if dx == 0:
            # Vertical line: x = constant
            return {"type": "vertical", "x": point1[0]}
        
        m = dy / dx
        b = point1[1] - m * point1[0]
        
        return {"type": "linear", "slope": m, "intercept": b}
    except ValueError as e:
        raise ValidationError(str(e))

def line_intersection(line1_point1, line1_point2, line2_point1, line2_point2):
    """Find the intersection point of two lines."""
    try:
        validate_line_2d(line1_point1, line1_point2, "line1_point1", "line1_point2")
        validate_line_2d(line2_point1, line2_point2, "line2_point1", "line2_point2")
        
        # Get line equations
        eq1 = line_equation(line1_point1, line1_point2)
        eq2 = line_equation(line2_point1, line2_point2)
        
        # Handle vertical lines
        if eq1["type"] == "vertical" and eq2["type"] == "vertical":
            if eq1["x"] == eq2["x"]:
                raise CalculationError("Lines are coincident (same vertical line).")
            else:
                raise CalculationError("Lines are parallel (different vertical lines).")
        
        if eq1["type"] == "vertical":
            x = eq1["x"]
            y = eq2["slope"] * x + eq2["intercept"]
            return (x, y)
        
        if eq2["type"] == "vertical":
            x = eq2["x"]
            y = eq1["slope"] * x + eq1["intercept"]
            return (x, y)
        
        # Both lines are non-vertical
        m1, b1 = eq1["slope"], eq1["intercept"]
        m2, b2 = eq2["slope"], eq2["intercept"]
        
        if m1 == m2:
            if b1 == b2:
                raise CalculationError("Lines are coincident (same line).")
            else:
                raise CalculationError("Lines are parallel (different slopes).")
        
        # Find intersection point
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
        
        return (x, y)
    except ValueError as e:
        raise ValidationError(str(e))

def point_to_line_distance(point, line_point1, line_point2):
    """Calculate the distance from a point to a line."""
    try:
        validate_2d_point(point, "point")
        validate_line_2d(line_point1, line_point2, "line_point1", "line_point2")
        
        x0, y0 = point
        x1, y1 = line_point1
        x2, y2 = line_point2
        
        # Calculate distance using the formula:
        # |ax0 + by0 + c| / sqrt(a^2 + b^2)
        # where ax + by + c = 0 is the line equation
        
        # Convert to standard form: ax + by + c = 0
        a = y2 - y1
        b = x1 - x2
        c = x2 * y1 - x1 * y2
        
        distance = abs(a * x0 + b * y0 + c) / math.sqrt(a**2 + b**2)
        return distance
    except ValueError as e:
        raise ValidationError(str(e))
