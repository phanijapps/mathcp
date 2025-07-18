"""Trigonometric functions for mathgenius."""

import math
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError

def validate_angle_domain(value, min_val=-1, max_val=1, name="value"):
    """Validate that a value is within the specified domain."""
    if not isinstance(value, (int, float)):
        raise ValueError(f"Invalid input: {name} must be a number.")
    if value < min_val or value > max_val:
        raise ValueError(f"Invalid input: {name} must be between {min_val} and {max_val}.")
    return value

# Angle Unit Conversion

def degrees_to_radians(degrees):
    """Convert degrees to radians."""
    try:
        validate_numbers(degrees)
        return math.radians(degrees)
    except ValueError as e:
        raise ValidationError(str(e))

def radians_to_degrees(radians):
    """Convert radians to degrees."""
    try:
        validate_numbers(radians)
        return math.degrees(radians)
    except ValueError as e:
        raise ValidationError(str(e))

# Basic Trigonometric Functions

def sin(angle, unit='radians'):
    """Calculate the sine of an angle."""
    try:
        validate_numbers(angle)
        if unit not in ['radians', 'degrees']:
            raise ValueError("Unit must be 'radians' or 'degrees'.")
        
        if unit == 'degrees':
            angle = degrees_to_radians(angle)
        
        return math.sin(angle)
    except ValueError as e:
        raise ValidationError(str(e))

def cos(angle, unit='radians'):
    """Calculate the cosine of an angle."""
    try:
        validate_numbers(angle)
        if unit not in ['radians', 'degrees']:
            raise ValueError("Unit must be 'radians' or 'degrees'.")
        
        if unit == 'degrees':
            angle = degrees_to_radians(angle)
        
        return math.cos(angle)
    except ValueError as e:
        raise ValidationError(str(e))

def tan(angle, unit='radians'):
    """Calculate the tangent of an angle."""
    try:
        validate_numbers(angle)
        if unit not in ['radians', 'degrees']:
            raise ValueError("Unit must be 'radians' or 'degrees'.")
        
        original_angle = angle
        if unit == 'degrees':
            angle = degrees_to_radians(angle)
        
        # Check for undefined values (odd multiples of π/2)
        if unit == 'degrees':
            # Check if angle is an odd multiple of 90 degrees
            normalized = abs(original_angle) % 180
            if abs(normalized - 90) < 1e-10:
                raise CalculationError("Tangent is undefined for odd multiples of 90 degrees.")
        else:
            # Check if angle is an odd multiple of π/2
            normalized = abs(angle) % math.pi
            if abs(normalized - math.pi/2) < 1e-10:
                raise CalculationError("Tangent is undefined for odd multiples of π/2.")
        
        return math.tan(angle)
    except ValueError as e:
        raise ValidationError(str(e))

# Inverse Trigonometric Functions

def asin(value, unit='radians'):
    """Calculate the arcsine of a value."""
    try:
        validate_angle_domain(value, -1, 1, "value")
        
        result = math.asin(value)
        
        if unit == 'degrees':
            result = radians_to_degrees(result)
        elif unit != 'radians':
            raise ValueError("Unit must be 'radians' or 'degrees'.")
        
        return result
    except ValueError as e:
        raise ValidationError(str(e))

def acos(value, unit='radians'):
    """Calculate the arccosine of a value."""
    try:
        validate_angle_domain(value, -1, 1, "value")
        
        result = math.acos(value)
        
        if unit == 'degrees':
            result = radians_to_degrees(result)
        elif unit != 'radians':
            raise ValueError("Unit must be 'radians' or 'degrees'.")
        
        return result
    except ValueError as e:
        raise ValidationError(str(e))

def atan(value, unit='radians'):
    """Calculate the arctangent of a value."""
    try:
        validate_numbers(value)
        
        result = math.atan(value)
        
        if unit == 'degrees':
            result = radians_to_degrees(result)
        elif unit != 'radians':
            raise ValueError("Unit must be 'radians' or 'degrees'.")
        
        return result
    except ValueError as e:
        raise ValidationError(str(e))

# Hyperbolic Trigonometric Functions

def sinh(value):
    """Calculate the hyperbolic sine of a value."""
    try:
        validate_numbers(value)
        return math.sinh(value)
    except ValueError as e:
        raise ValidationError(str(e))

def cosh(value):
    """Calculate the hyperbolic cosine of a value."""
    try:
        validate_numbers(value)
        return math.cosh(value)
    except ValueError as e:
        raise ValidationError(str(e))

def tanh(value):
    """Calculate the hyperbolic tangent of a value."""
    try:
        validate_numbers(value)
        return math.tanh(value)
    except ValueError as e:
        raise ValidationError(str(e))
