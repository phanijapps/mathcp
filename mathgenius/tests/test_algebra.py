import pytest
from mathgenius.algebra.equations import solve_linear, solve_quadratic
from mathgenius.algebra.polynomials import expand_expr, factor_expr, simplify_expr
from mathgenius.core.errors import ValidationError
from sympy import symbols

def test_solve_linear():
    assert solve_linear(2, -4) == 2
    with pytest.raises(ValidationError):
        solve_linear("a", 1)

def test_solve_quadratic():
    roots = solve_quadratic(1, -3, 2)
    assert set(roots) == {1, 2}
    with pytest.raises(ValidationError):
        solve_quadratic(1, "b", 2)

def test_expand_expr():
    x = symbols('x')
    assert expand_expr((x + 1)**2) == x**2 + 2*x + 1
    with pytest.raises(ValidationError):
        expand_expr(None)

def test_factor_expr():
    x = symbols('x')
    assert factor_expr(x**2 + 2*x + 1) == (x + 1)**2
    with pytest.raises(ValidationError):
        factor_expr(None)

def test_simplify_expr():
    x = symbols('x')
    assert simplify_expr((x**2 + 2*x + 1)/(x + 1)) == x + 1
    with pytest.raises(ValidationError):
        simplify_expr(None)
