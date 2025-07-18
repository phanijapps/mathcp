"""Equation solving functions for mathgenius."""
from sympy import symbols, Eq, solve
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError

def solve_linear(a, b):
    try:
        validate_numbers(a, b)
        x = symbols('x')
        eq = Eq(a * x + b, 0)
        sol = solve(eq, x)
        return sol[0] if sol else None
    except Exception as e:
        raise ValidationError(str(e))

def solve_quadratic(a, b, c):
    try:
        validate_numbers(a, b, c)
        x = symbols('x')
        eq = Eq(a * x**2 + b * x + c, 0)
        sol = solve(eq, x)
        return sol
    except Exception as e:
        raise ValidationError(str(e))
