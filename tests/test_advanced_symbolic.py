"""Test suite for advanced symbolic mathematics operations."""
import pytest
import sympy as sp
from mathgenius.advanced.symbolic import (
    parse_expression, create_symbol, expand_expression, factor_expression,
    simplify_expression, collect_terms, solve_equation, solve_differential_equation,
    substitute_expression, evaluate_expression, expression_to_latex,
    expression_to_string, symbolic_integrate, symbolic_differentiate,
    symbolic_limit, symbolic_series, create_rational, is_polynomial
)
from mathgenius.core.errors import ValidationError, CalculationError


class TestExpressionParsing:
    """Test expression parsing and creation."""
    
    def test_parse_expression_basic(self):
        """Test basic expression parsing."""
        expr = parse_expression("x**2 + 2*x + 1")
        assert isinstance(expr, sp.Expr)
        assert str(expr) == "x**2 + 2*x + 1"
    
    def test_parse_expression_trigonometric(self):
        """Test parsing trigonometric expressions."""
        expr = parse_expression("sin(x) + cos(x)")
        assert isinstance(expr, sp.Expr)
        assert "sin(x)" in str(expr)
        assert "cos(x)" in str(expr)
    
    def test_parse_expression_empty(self):
        """Test parsing empty expression."""
        with pytest.raises(ValidationError):
            parse_expression("")
    
    def test_parse_expression_invalid_type(self):
        """Test parsing with invalid type."""
        with pytest.raises(ValidationError):
            parse_expression(123)
    
    def test_parse_expression_invalid_syntax(self):
        """Test parsing with invalid syntax."""
        with pytest.raises(CalculationError):
            parse_expression("x + + y")
    
    def test_create_symbol_basic(self):
        """Test basic symbol creation."""
        symbol = create_symbol("x")
        assert isinstance(symbol, sp.Symbol)
        assert str(symbol) == "x"
    
    def test_create_symbol_with_assumptions(self):
        """Test symbol creation with assumptions."""
        symbol = create_symbol("x", {"real": True, "positive": True})
        assert isinstance(symbol, sp.Symbol)
        assert symbol.is_real == True
        assert symbol.is_positive == True
    
    def test_create_symbol_empty_name(self):
        """Test creating symbol with empty name."""
        with pytest.raises(ValidationError):
            create_symbol("")
    
    def test_create_symbol_invalid_type(self):
        """Test creating symbol with invalid type."""
        with pytest.raises(ValidationError):
            create_symbol(123)


class TestExpressionManipulation:
    """Test expression manipulation functions."""
    
    def test_expand_expression_basic(self):
        """Test basic expression expansion."""
        expr = "(x + 1)**2"
        result = expand_expression(expr)
        expected = "x**2 + 2*x + 1"
        assert str(result) == expected
    
    def test_expand_expression_sympy_object(self):
        """Test expansion with SymPy object."""
        x = sp.Symbol('x')
        expr = (x + 1)**2
        result = expand_expression(expr)
        expected = x**2 + 2*x + 1
        assert result == expected
    
    def test_factor_expression_basic(self):
        """Test basic expression factoring."""
        expr = "x**2 + 2*x + 1"
        result = factor_expression(expr)
        expected = "(x + 1)**2"
        assert str(result) == expected
    
    def test_factor_expression_quadratic(self):
        """Test factoring quadratic expression."""
        expr = "x**2 - 1"
        result = factor_expression(expr)
        expected = "(x - 1)*(x + 1)"
        assert str(result) == expected
    
    def test_simplify_expression_basic(self):
        """Test basic expression simplification."""
        expr = "x + x + x"
        result = simplify_expression(expr)
        expected = "3*x"
        assert str(result) == expected
    
    def test_simplify_expression_trigonometric(self):
        """Test trigonometric expression simplification."""
        expr = "sin(x)**2 + cos(x)**2"
        result = simplify_expression(expr)
        expected = "1"
        assert str(result) == expected
    
    def test_collect_terms_basic(self):
        """Test term collection."""
        expr = "x**2 + 2*x*y + y**2"
        result = collect_terms(expr, "x")
        # Should collect terms with respect to x
        result_str = str(result)
        assert "x**2" in result_str
        assert "2*y*x" in result_str or "2*x*y" in result_str
    
    def test_collect_terms_invalid_variable(self):
        """Test term collection with invalid variable."""
        expr = "x**2 + 2*x + 1"
        with pytest.raises(ValidationError):
            collect_terms(expr, 123)


class TestEquationSolving:
    """Test equation solving functions."""
    
    def test_solve_equation_linear(self):
        """Test solving linear equation."""
        equation = "2*x + 3 - 7"
        result = solve_equation(equation, "x")
        expected = [2]  # x = 2
        assert result == expected
    
    def test_solve_equation_quadratic(self):
        """Test solving quadratic equation."""
        equation = "x**2 - 5*x + 6"
        result = solve_equation(equation, "x")
        expected = [2, 3]  # x = 2 or x = 3
        assert sorted(result) == sorted(expected)
    
    def test_solve_equation_system(self):
        """Test solving system of equations."""
        equations = ["x + y - 3", "2*x - y"]
        result = solve_equation(equations, ["x", "y"])
        # Should be x = 1, y = 2
        expected = {sp.Symbol('x'): 1, sp.Symbol('y'): 2}
        assert len(result) == 1
        assert result[0] == expected
    
    def test_solve_equation_no_solution(self):
        """Test solving equation with no solution."""
        equation = "x + 1 - x"  # 1 = 0, no solution
        result = solve_equation(equation, "x")
        assert result == []
    
    def test_solve_differential_equation_basic(self):
        """Test solving basic differential equation."""
        # dy/dx = y
        equation = "Derivative(y(x), x) - y(x)"
        result = solve_differential_equation(equation, "y")
        
        # Should contain exponential function
        result_str = str(result)
        assert "exp" in result_str
        assert "C1" in result_str  # Integration constant


class TestSubstitutionEvaluation:
    """Test substitution and evaluation functions."""
    
    def test_substitute_expression_basic(self):
        """Test basic substitution."""
        expr = "x**2 + 2*x + 1"
        substitutions = {"x": 3}
        result = substitute_expression(expr, substitutions)
        expected = 16  # 3**2 + 2*3 + 1 = 16
        assert result == expected
    
    def test_substitute_expression_multiple_variables(self):
        """Test substitution with multiple variables."""
        expr = "x**2 + y**2"
        substitutions = {"x": 3, "y": 4}
        result = substitute_expression(expr, substitutions)
        expected = 25  # 3**2 + 4**2 = 25
        assert result == expected
    
    def test_substitute_expression_symbolic(self):
        """Test symbolic substitution."""
        expr = "x**2 + 2*x + 1"
        substitutions = {"x": "y + 1"}
        result = substitute_expression(expr, substitutions)
        # Should substitute y+1 for x
        result_str = str(result)
        assert "y" in result_str
    
    def test_substitute_expression_invalid_substitutions(self):
        """Test substitution with invalid substitutions."""
        expr = "x**2 + 2*x + 1"
        with pytest.raises(ValidationError):
            substitute_expression(expr, "not_a_dict")
    
    def test_evaluate_expression_basic(self):
        """Test basic expression evaluation."""
        expr = "2 + 3 * 4"
        result = evaluate_expression(expr)
        expected = 14
        assert result == expected
    
    def test_evaluate_expression_with_substitutions(self):
        """Test evaluation with substitutions."""
        expr = "x**2 + 2*x + 1"
        substitutions = {"x": 3}
        result = evaluate_expression(expr, substitutions)
        expected = 16.0
        assert abs(result - expected) < 1e-10
    
    def test_evaluate_expression_complex(self):
        """Test evaluation resulting in complex number."""
        expr = "sqrt(-1)"
        result = evaluate_expression(expr)
        assert isinstance(result, complex)
        assert abs(result - 1j) < 1e-10


class TestExpressionFormatting:
    """Test expression formatting functions."""
    
    def test_expression_to_latex_basic(self):
        """Test LaTeX conversion."""
        expr = "x**2 + 2*x + 1"
        result = expression_to_latex(expr)
        assert "x^{2}" in result
        assert "2 x" in result
    
    def test_expression_to_latex_fraction(self):
        """Test LaTeX conversion with fractions."""
        expr = "x/y"
        result = expression_to_latex(expr)
        assert "\\frac" in result
    
    def test_expression_to_string_basic(self):
        """Test string conversion."""
        expr = "x**2 + 2*x + 1"
        result = expression_to_string(expr)
        assert "x**2" in result
        assert "2*x" in result
    
    def test_expression_to_string_pretty(self):
        """Test pretty string conversion."""
        expr = "x**2 + 2*x + 1"
        result = expression_to_string(expr, pretty_print=True)
        # Pretty print should produce multi-line string for complex expressions
        assert isinstance(result, str)


class TestSymbolicCalculus:
    """Test symbolic calculus functions."""
    
    def test_symbolic_integrate_indefinite(self):
        """Test indefinite symbolic integration."""
        expr = "x**2"
        result = symbolic_integrate(expr, "x")
        expected = "x**3/3"
        assert str(result) == expected
    
    def test_symbolic_integrate_definite(self):
        """Test definite symbolic integration."""
        expr = "x**2"
        result = symbolic_integrate(expr, "x", limits=(0, 1))
        expected = sp.Rational(1, 3)
        assert result == expected
    
    def test_symbolic_integrate_invalid_limits(self):
        """Test integration with invalid limits."""
        expr = "x**2"
        with pytest.raises(ValidationError):
            symbolic_integrate(expr, "x", limits=(0,))  # Only one limit
    
    def test_symbolic_differentiate_basic(self):
        """Test symbolic differentiation."""
        expr = "x**3"
        result = symbolic_differentiate(expr, "x")
        expected = "3*x**2"
        assert str(result) == expected
    
    def test_symbolic_differentiate_higher_order(self):
        """Test higher order symbolic differentiation."""
        expr = "x**4"
        result = symbolic_differentiate(expr, "x", order=2)
        expected = "12*x**2"
        assert str(result) == expected
    
    def test_symbolic_differentiate_invalid_order(self):
        """Test differentiation with invalid order."""
        expr = "x**2"
        with pytest.raises(ValidationError):
            symbolic_differentiate(expr, "x", order=0)
    
    def test_symbolic_limit_basic(self):
        """Test symbolic limit calculation."""
        expr = "sin(x)/x"
        result = symbolic_limit(expr, "x", 0)
        expected = 1
        assert result == expected
    
    def test_symbolic_limit_infinity(self):
        """Test limit at infinity."""
        expr = "1/x"
        result = symbolic_limit(expr, "x", "oo")
        expected = 0
        assert result == expected
    
    def test_symbolic_limit_invalid_direction(self):
        """Test limit with invalid direction."""
        expr = "x"
        with pytest.raises(ValidationError):
            symbolic_limit(expr, "x", 0, direction="invalid")
    
    def test_symbolic_series_basic(self):
        """Test symbolic series expansion."""
        expr = "exp(x)"
        result = symbolic_series(expr, "x", 0, 4)
        # Should contain terms 1, x, x^2/2, x^3/6, x^4/24
        result_str = str(result)
        assert "1" in result_str
        assert "x" in result_str
        assert "x**2" in result_str
    
    def test_symbolic_series_invalid_order(self):
        """Test series with invalid order."""
        expr = "exp(x)"
        with pytest.raises(ValidationError):
            symbolic_series(expr, "x", 0, -1)


class TestRationalNumbers:
    """Test rational number functions."""
    
    def test_create_rational_basic(self):
        """Test basic rational number creation."""
        result = create_rational(3, 4)
        assert result == sp.Rational(3, 4)
        assert str(result) == "3/4"
    
    def test_create_rational_simplification(self):
        """Test rational number simplification."""
        result = create_rational(6, 8)
        expected = sp.Rational(3, 4)
        assert result == expected
    
    def test_create_rational_zero_denominator(self):
        """Test rational with zero denominator."""
        with pytest.raises(ValidationError):
            create_rational(3, 0)
    
    def test_create_rational_invalid_types(self):
        """Test rational with invalid types."""
        with pytest.raises(ValidationError):
            create_rational(3.5, 4)
        
        with pytest.raises(ValidationError):
            create_rational(3, "4")


class TestPolynomialCheck:
    """Test polynomial checking function."""
    
    def test_is_polynomial_basic(self):
        """Test basic polynomial checking."""
        expr = "x**2 + 2*x + 1"
        result = is_polynomial(expr, "x")
        assert result == True
    
    def test_is_polynomial_not_polynomial(self):
        """Test non-polynomial expression."""
        expr = "sin(x)"
        result = is_polynomial(expr, "x")
        assert result == False
    
    def test_is_polynomial_rational_function(self):
        """Test rational function (not polynomial)."""
        expr = "1/x"
        result = is_polynomial(expr, "x")
        assert result == False
    
    def test_is_polynomial_constant(self):
        """Test constant expression."""
        expr = "5"
        result = is_polynomial(expr)
        assert result == True
    
    def test_is_polynomial_multivariable(self):
        """Test multivariable polynomial."""
        expr = "x**2 + y**2 + x*y"
        result = is_polynomial(expr)
        assert result == True


if __name__ == "__main__":
    pytest.main([__file__])
