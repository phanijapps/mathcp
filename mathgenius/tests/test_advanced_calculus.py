"""Test suite for advanced calculus operations."""
import pytest
import math
import numpy as np
from mathgenius.advanced.calculus import (
    differentiate, integrate_definite, integrate_indefinite, compute_limit,
    taylor_series, partial_derivative, gradient, hessian_matrix,
    numerical_derivative, numerical_integral
)
from mathgenius.core.errors import ValidationError, CalculationError


class TestDifferentiation:
    """Test differentiation functions."""
    
    def test_differentiate_basic(self):
        """Test basic differentiation."""
        # Test x^2 -> 2*x
        result = differentiate("x**2", "x")
        assert str(result) == "2*x"
        
        # Test sin(x) -> cos(x)
        result = differentiate("sin(x)", "x")
        assert str(result) == "cos(x)"
        
        # Test e^x -> e^x
        result = differentiate("exp(x)", "x")
        assert str(result) == "exp(x)"
    
    def test_differentiate_higher_order(self):
        """Test higher order derivatives."""
        # Test second derivative of x^3
        result = differentiate("x**3", "x", order=2)
        assert str(result) == "6*x"
        
        # Test third derivative of x^3
        result = differentiate("x**3", "x", order=3)
        assert str(result) == "6"
    
    def test_differentiate_invalid_order(self):
        """Test differentiation with invalid order."""
        with pytest.raises(ValidationError):
            differentiate("x**2", "x", order=0)
        
        with pytest.raises(ValidationError):
            differentiate("x**2", "x", order=-1)
    
    def test_differentiate_invalid_expression(self):
        """Test differentiation with invalid expression."""
        with pytest.raises(ValidationError):
            differentiate("**x", "x")


class TestIntegration:
    """Test integration functions."""
    
    def test_integrate_indefinite_basic(self):
        """Test basic indefinite integration."""
        # Test integral of x -> x^2/2
        result = integrate_indefinite("x", "x")
        assert str(result) == "x**2/2"
        
        # Test integral of x^2 -> x^3/3
        result = integrate_indefinite("x**2", "x")
        assert str(result) == "x**3/3"
    
    def test_integrate_definite_basic(self):
        """Test basic definite integration."""
        # Test integral of x from 0 to 1 -> 1/2
        result = integrate_definite("x", "x", 0, 1)
        assert abs(result - 0.5) < 1e-10
        
        # Test integral of x^2 from 0 to 2 -> 8/3
        result = integrate_definite("x**2", "x", 0, 2)
        assert abs(result - 8/3) < 1e-10
    
    def test_integrate_definite_invalid_bounds(self):
        """Test definite integration with invalid bounds."""
        with pytest.raises(ValidationError):
            integrate_definite("x", "x", "invalid", 1)
    
    def test_integrate_invalid_expression(self):
        """Test integration with invalid expression."""
        with pytest.raises(ValidationError):
            integrate_indefinite("x**", "x")


class TestLimits:
    """Test limit calculations."""
    
    def test_compute_limit_basic(self):
        """Test basic limit calculations."""
        # Test limit of x as x approaches 0
        result = compute_limit("x", "x", 0)
        assert result == 0
        
        # Test limit of x^2 as x approaches 2
        result = compute_limit("x**2", "x", 2)
        assert result == 4
    
    def test_compute_limit_infinity(self):
        """Test limits involving infinity."""
        # Test limit of 1/x as x approaches infinity
        result = compute_limit("1/x", "x", "oo")
        assert result == 0
    
    def test_compute_limit_invalid_direction(self):
        """Test limit with invalid direction."""
        with pytest.raises(ValidationError):
            compute_limit("x", "x", 0, direction="invalid")
    
    def test_compute_limit_invalid_expression(self):
        """Test limit with invalid expression."""
        with pytest.raises(ValidationError):
            compute_limit("++", "x", 0)


class TestTaylorSeries:
    """Test Taylor series expansion."""
    
    def test_taylor_series_basic(self):
        """Test basic Taylor series."""
        # Test Taylor series of e^x around x=0
        result = taylor_series("exp(x)", "x", 0, 4)
        # Should be approximately 1 + x + x^2/2 + x^3/6 + x^4/24
        expected_terms = ["1", "x", "x**2/2", "x**3/6", "x**4/24"]
        result_str = str(result)
        assert "1" in result_str
        assert "x" in result_str
        assert "x**2" in result_str
    
    def test_taylor_series_invalid_order(self):
        """Test Taylor series with invalid order."""
        with pytest.raises(ValidationError):
            taylor_series("exp(x)", "x", 0, -1)
    
    def test_taylor_series_invalid_point(self):
        """Test Taylor series with invalid point."""
        with pytest.raises(ValidationError):
            taylor_series("exp(x)", "x", "invalid", 4)


class TestMultivariableCalculus:
    """Test multivariable calculus functions."""
    
    def test_partial_derivative_basic(self):
        """Test basic partial derivatives."""
        # Test partial derivative of x^2 + y^2 with respect to x -> 2*x
        result = partial_derivative("x**2 + y**2", "x")
        assert str(result) == "2*x"
        
        # Test partial derivative of x^2 + y^2 with respect to y -> 2*y
        result = partial_derivative("x**2 + y**2", "y")
        assert str(result) == "2*y"
    
    def test_gradient_basic(self):
        """Test gradient calculation."""
        # Test gradient of x^2 + y^2
        result = gradient("x**2 + y**2", ["x", "y"])
        assert len(result) == 2
        assert str(result[0]) == "2*x"
        assert str(result[1]) == "2*y"
    
    def test_hessian_matrix_basic(self):
        """Test Hessian matrix calculation."""
        # Test Hessian of x^2 + y^2
        result = hessian_matrix("x**2 + y**2", ["x", "y"])
        assert result.shape == (2, 2)
        assert str(result[0, 0]) == "2"
        assert str(result[1, 1]) == "2"
        assert str(result[0, 1]) == "0"
        assert str(result[1, 0]) == "0"
    
    def test_gradient_invalid_variables(self):
        """Test gradient with invalid variables."""
        with pytest.raises(ValidationError):
            gradient("x**2 + y**2", [])
        
        with pytest.raises(ValidationError):
            gradient("x**2 + y**2", [123])


class TestNumericalMethods:
    """Test numerical calculus methods."""
    
    def test_numerical_derivative_basic(self):
        """Test numerical derivative calculation."""
        # Test derivative of x^2 at x=2 (should be 4)
        def f(x):
            return x**2
        
        result = numerical_derivative(f, 2)
        assert abs(result - 4) < 1e-6
    
    def test_numerical_derivative_invalid_function(self):
        """Test numerical derivative with invalid function."""
        with pytest.raises(ValidationError):
            numerical_derivative("not_a_function", 2)
    
    def test_numerical_derivative_invalid_step(self):
        """Test numerical derivative with invalid step size."""
        def f(x):
            return x**2
        
        with pytest.raises(ValidationError):
            numerical_derivative(f, 2, h=0)
        
        with pytest.raises(ValidationError):
            numerical_derivative(f, 2, h=-1)
    
    def test_numerical_integral_basic(self):
        """Test numerical integration methods."""
        # Test integral of x^2 from 0 to 1 (should be 1/3)
        def f(x):
            return x**2
        
        # Test Simpson's rule
        result = numerical_integral(f, 0, 1, method='simpson', n=1000)
        assert abs(result - 1/3) < 1e-6
        
        # Test trapezoidal rule
        result = numerical_integral(f, 0, 1, method='trapezoidal', n=1000)
        assert abs(result - 1/3) < 1e-4
        
        # Test midpoint rule
        result = numerical_integral(f, 0, 1, method='midpoint', n=1000)
        assert abs(result - 1/3) < 1e-4
    
    def test_numerical_integral_invalid_method(self):
        """Test numerical integration with invalid method."""
        def f(x):
            return x**2
        
        with pytest.raises(ValidationError):
            numerical_integral(f, 0, 1, method='invalid')
    
    def test_numerical_integral_invalid_function(self):
        """Test numerical integration with invalid function."""
        with pytest.raises(ValidationError):
            numerical_integral("not_a_function", 0, 1)
    
    def test_numerical_integral_invalid_intervals(self):
        """Test numerical integration with invalid intervals."""
        def f(x):
            return x**2
        
        with pytest.raises(ValidationError):
            numerical_integral(f, 0, 1, n=0)
        
        with pytest.raises(ValidationError):
            numerical_integral(f, 0, 1, n=-1)


if __name__ == "__main__":
    pytest.main([__file__])
