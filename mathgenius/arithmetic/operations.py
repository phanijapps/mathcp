"""Basic arithmetic operations for mathgenius."""
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError

def add(a, b):
    try:
        validate_numbers(a, b)
        return a + b
    except ValueError as e:
        raise ValidationError(str(e))

def subtract(a, b):
    try:
        validate_numbers(a, b)
        return a - b
    except ValueError as e:
        raise ValidationError(str(e))

def multiply(a, b):
    try:
        validate_numbers(a, b)
        return a * b
    except ValueError as e:
        raise ValidationError(str(e))

def divide(a, b):
    try:
        validate_numbers(a, b)
        if b == 0:
            raise CalculationError("Division by zero.")
        return a / b
    except ValueError as e:
        raise ValidationError(str(e))

def power(a, b):
    try:
        validate_numbers(a, b)
        return a ** b
    except ValueError as e:
        raise ValidationError(str(e))

def modulo(a, b):
    try:
        validate_numbers(a, b)
        if b == 0:
            raise CalculationError("Modulo by zero.")
        return a % b
    except ValueError as e:
        raise ValidationError(str(e))
