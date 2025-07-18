"""Custom exceptions for mathgenius modules."""

class MathGeniusError(Exception):
    """Base exception for mathgenius library."""
    pass

class ValidationError(MathGeniusError):
    """Exception for input validation errors."""
    pass

class CalculationError(MathGeniusError):
    """Exception for calculation errors."""
    pass
