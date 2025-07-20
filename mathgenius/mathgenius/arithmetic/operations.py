"""Basic arithmetic operations for mathgenius.

Each function validates numeric input and raises :class:`ValidationError`
on invalid arguments. Examples below demonstrate typical usage within
Python code.
"""
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError

def add(a, b):
    """Return the sum of ``a`` and ``b``.

    Parameters
    ----------
    a : int | float
        First operand.
    b : int | float
        Second operand.

    Returns
    -------
    int | float
        The sum ``a + b``.

    Raises
    ------
    ValidationError
        If either input is not numeric.

    Examples
    --------
    >>> add(2, 3)
    5
    """
    try:
        validate_numbers(a, b)
        return a + b
    except ValueError as e:
        raise ValidationError(str(e))

def subtract(a, b):
    """Return the difference of ``a`` and ``b``.

    Parameters
    ----------
    a : int | float
        Minuend.
    b : int | float
        Subtrahend.

    Returns
    -------
    int | float
        The result ``a - b``.

    Raises
    ------
    ValidationError
        If either input is not numeric.

    Examples
    --------
    >>> subtract(5, 2)
    3
    """
    try:
        validate_numbers(a, b)
        return a - b
    except ValueError as e:
        raise ValidationError(str(e))

def multiply(a, b):
    """Return the product of ``a`` and ``b``.

    Parameters
    ----------
    a : int | float
        First factor.
    b : int | float
        Second factor.

    Returns
    -------
    int | float
        The result ``a * b``.

    Raises
    ------
    ValidationError
        If either input is not numeric.

    Examples
    --------
    >>> multiply(4, 3)
    12
    """
    try:
        validate_numbers(a, b)
        return a * b
    except ValueError as e:
        raise ValidationError(str(e))

def divide(a, b):
    """Return the quotient of ``a`` divided by ``b``.

    Parameters
    ----------
    a : int | float
        Dividend.
    b : int | float
        Divisor.

    Returns
    -------
    float
        The result ``a / b``.

    Raises
    ------
    ValidationError
        If either input is not numeric.
    
    CalculationError
        If ``b`` is zero.

    Examples
    --------
    >>> divide(10, 2)
    5.0
    """
    try:
        validate_numbers(a, b)
        if b == 0:
            raise CalculationError("Division by zero.")
        return a / b
    except ValueError as e:
        raise ValidationError(str(e))

def power(a, b):
    """Return ``a`` raised to the power ``b``.

    Parameters
    ----------
    a : int | float
        Base value.
    b : int | float
        Exponent value.

    Returns
    -------
    int | float
        Result of ``a ** b``.

    Raises
    ------
    ValidationError
        If either input is not numeric.

    Examples
    --------
    >>> power(2, 3)
    8
    """
    try:
        validate_numbers(a, b)
        return a ** b
    except ValueError as e:
        raise ValidationError(str(e))

def modulo(a, b):
    """Return the remainder of ``a`` divided by ``b``.

    Parameters
    ----------
    a : int | float
        Dividend.
    b : int | float
        Divisor.

    Returns
    -------
    int | float
        The remainder ``a % b``.

    Raises
    ------
    ValidationError
        If either input is not numeric.
    
    CalculationError
        If ``b`` is zero.

    Examples
    --------
    >>> modulo(10, 3)
    1
    """
    try:
        validate_numbers(a, b)
        if b == 0:
            raise CalculationError("Modulo by zero.")
        return a % b
    except ValueError as e:
        raise ValidationError(str(e))
