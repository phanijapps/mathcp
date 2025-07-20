"""Polynomial operations for mathgenius."""
from sympy import expand, factor, simplify, symbols
from mathgenius.core.errors import ValidationError

def expand_expr(expr):
    try:
        return expand(expr)
    except Exception as e:
        raise ValidationError(str(e))

def factor_expr(expr):
    if expr is None:
        raise ValidationError("Input expression cannot be None.")
    try:
        return factor(expr)
    except Exception as e:
        raise ValidationError(str(e))

def simplify_expr(expr):
    try:
        return simplify(expr)
    except Exception as e:
        raise ValidationError(str(e))
