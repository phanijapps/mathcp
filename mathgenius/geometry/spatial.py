"""Spatial operations for mathgenius."""

import math
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError

def validate_vector(vector, dimensions=None, name="vector"):
    """Validate a vector (2D or 3D)."""
    if not isinstance(vector, (list, tuple)):
        raise ValueError(f"Invalid input: {name} must be a list or tuple.")
    
    if dimensions is not None and len(vector) != dimensions:
        raise ValueError(f"Invalid input: {name} must have {dimensions} dimensions.")
    
    if len(vector) not in [2, 3]:
        raise ValueError(f"Invalid input: {name} must be 2D or 3D.")
    
    for i, component in enumerate(vector):
        if not isinstance(component, (int, float)):
            raise ValueError(f"Invalid input: {name}[{i}] must be a number.")
    
    return vector

def validate_vectors_same_dimension(vector1, vector2, name1="vector1", name2="vector2"):
    """Validate two vectors have the same dimensions."""
    validate_vector(vector1, name=name1)
    validate_vector(vector2, name=name2)
    
    if len(vector1) != len(vector2):
        raise ValueError(f"Invalid input: {name1} and {name2} must have the same dimensions.")
    
    return vector1, vector2

def validate_non_zero_vector(vector, name="vector"):
    """Validate that a vector is not zero."""
    validate_vector(vector, name=name)
    
    if all(component == 0 for component in vector):
        raise ValueError(f"Invalid input: {name} cannot be a zero vector.")
    
    return vector

# Vector Operations

def vector_add(vector1, vector2):
    """Add two vectors."""
    try:
        validate_vectors_same_dimension(vector1, vector2)
        
        result = [vector1[i] + vector2[i] for i in range(len(vector1))]
        return tuple(result)
    except ValueError as e:
        raise ValidationError(str(e))

def vector_subtract(vector1, vector2):
    """Subtract vector2 from vector1."""
    try:
        validate_vectors_same_dimension(vector1, vector2)
        
        result = [vector1[i] - vector2[i] for i in range(len(vector1))]
        return tuple(result)
    except ValueError as e:
        raise ValidationError(str(e))

def vector_dot_product(vector1, vector2):
    """Calculate the dot product of two vectors."""
    try:
        validate_vectors_same_dimension(vector1, vector2)
        
        return sum(vector1[i] * vector2[i] for i in range(len(vector1)))
    except ValueError as e:
        raise ValidationError(str(e))

def vector_cross_product(vector1, vector2):
    """Calculate the cross product of two 3D vectors."""
    try:
        validate_vector(vector1, dimensions=3, name="vector1")
        validate_vector(vector2, dimensions=3, name="vector2")
        
        x = vector1[1] * vector2[2] - vector1[2] * vector2[1]
        y = vector1[2] * vector2[0] - vector1[0] * vector2[2]
        z = vector1[0] * vector2[1] - vector1[1] * vector2[0]
        
        return (x, y, z)
    except ValueError as e:
        raise ValidationError(str(e))

def vector_magnitude(vector):
    """Calculate the magnitude (length) of a vector."""
    try:
        validate_vector(vector)
        
        return math.sqrt(sum(component**2 for component in vector))
    except ValueError as e:
        raise ValidationError(str(e))

def vector_normalize(vector):
    """Normalize a vector to unit length."""
    try:
        validate_non_zero_vector(vector)
        
        magnitude = vector_magnitude(vector)
        if magnitude == 0:
            raise CalculationError("Cannot normalize zero vector.")
        
        result = [component / magnitude for component in vector]
        return tuple(result)
    except ValueError as e:
        raise ValidationError(str(e))

# Angle Calculations

def angle_between_vectors(vector1, vector2, unit='radians'):
    """Calculate the angle between two vectors."""
    try:
        validate_non_zero_vector(vector1, "vector1")
        validate_non_zero_vector(vector2, "vector2")
        validate_vectors_same_dimension(vector1, vector2)
        
        if unit not in ['radians', 'degrees']:
            raise ValueError("Unit must be 'radians' or 'degrees'.")
        
        dot_product = vector_dot_product(vector1, vector2)
        magnitude1 = vector_magnitude(vector1)
        magnitude2 = vector_magnitude(vector2)
        
        # Calculate cosine of angle
        cos_angle = dot_product / (magnitude1 * magnitude2)
        
        # Clamp to [-1, 1] to avoid numerical errors
        cos_angle = max(-1, min(1, cos_angle))
        
        angle = math.acos(cos_angle)
        
        if unit == 'degrees':
            angle = math.degrees(angle)
        
        return angle
    except ValueError as e:
        raise ValidationError(str(e))

# Geometric Transformations

def rotate_point(point, angle, origin=(0, 0), unit='radians'):
    """Rotate a 2D point around an origin."""
    try:
        validate_vector(point, dimensions=2, name="point")
        validate_vector(origin, dimensions=2, name="origin")
        validate_numbers(angle)
        
        if unit not in ['radians', 'degrees']:
            raise ValueError("Unit must be 'radians' or 'degrees'.")
        
        if unit == 'degrees':
            angle = math.radians(angle)
        
        # Translate point to origin
        translated_x = point[0] - origin[0]
        translated_y = point[1] - origin[1]
        
        # Apply rotation
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        
        rotated_x = translated_x * cos_angle - translated_y * sin_angle
        rotated_y = translated_x * sin_angle + translated_y * cos_angle
        
        # Translate back
        final_x = rotated_x + origin[0]
        final_y = rotated_y + origin[1]
        
        return (final_x, final_y)
    except ValueError as e:
        raise ValidationError(str(e))

def translate_point(point, translation_vector):
    """Translate a point by a translation vector."""
    try:
        validate_vectors_same_dimension(point, translation_vector, "point", "translation_vector")
        
        result = [point[i] + translation_vector[i] for i in range(len(point))]
        return tuple(result)
    except ValueError as e:
        raise ValidationError(str(e))

def scale_point(point, scale_factor, origin=(0, 0)):
    """Scale a point from an origin."""
    try:
        validate_vector(point, name="point")
        validate_numbers(scale_factor)
        
        if len(point) == 2:
            validate_vector(origin, dimensions=2, name="origin")
        elif len(point) == 3:
            if len(origin) == 2:
                origin = (origin[0], origin[1], 0)
            validate_vector(origin, dimensions=3, name="origin")
        
        # Translate to origin, scale, then translate back
        translated = [point[i] - origin[i] for i in range(len(point))]
        scaled = [translated[i] * scale_factor for i in range(len(point))]
        result = [scaled[i] + origin[i] for i in range(len(point))]
        
        return tuple(result)
    except ValueError as e:
        raise ValidationError(str(e))
