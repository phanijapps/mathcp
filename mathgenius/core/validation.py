"""Input validation utilities for mathgenius modules."""
from .errors import ValidationError

def validate_number(value):
    if not isinstance(value, (int, float)):
        raise ValidationError(f"Invalid input: {value} is not a number.")
    return value

def validate_numbers(*values):
    for v in values:
        validate_number(v)
    return values
