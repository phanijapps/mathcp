"""Calculus operations module for advanced mathematical computations."""
import sympy as sp
import numpy as np
from sympy import symbols, diff, integrate, limit, series, oo, nan, zoo
from sympy.abc import x, y, z
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError


def differentiate(expression, variable='x', order=1):
    """
    Compute symbolic or numerical derivative of an expression.
    
    Args:
        expression (str|sympy.Expr): Mathematical expression to differentiate
        variable (str): Variable to differentiate with respect to
        order (int): Order of differentiation
        
    Returns:
        sympy.Expr: Derivative of the expression
        
    Raises:
        ValidationError: If expression or variable is invalid
        CalculationError: If differentiation fails
    """
    try:
        # Validate inputs
        if not isinstance(order, int) or order < 1:
            raise ValidationError("Order must be a positive integer")
            
        # Parse expression if it's a string
        if isinstance(expression, str):
            try:
                expr = sp.sympify(expression)
            except Exception:
                raise ValidationError(f"Invalid mathematical expression: {expression}")
        else:
            expr = expression
            
        # Validate variable
        if not isinstance(variable, str):
            raise ValidationError("Variable must be a string")
            
        var = symbols(variable)
        
        # Compute derivative
        result = diff(expr, var, order)
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute derivative: {str(e)}")


def integrate_definite(expression, variable='x', lower_bound=0, upper_bound=1):
    """
    Compute definite integral of an expression.
    
    Args:
        expression (str|sympy.Expr): Mathematical expression to integrate
        variable (str): Variable to integrate with respect to
        lower_bound (float): Lower bound of integration
        upper_bound (float): Upper bound of integration
        
    Returns:
        sympy.Expr|float: Definite integral value
        
    Raises:
        ValidationError: If expression or bounds are invalid
        CalculationError: If integration fails
    """
    try:
        # Validate bounds
        validate_numbers(lower_bound, upper_bound)
        
        # Parse expression if it's a string
        if isinstance(expression, str):
            try:
                expr = sp.sympify(expression)
            except Exception:
                raise ValidationError(f"Invalid mathematical expression: {expression}")
        else:
            expr = expression
            
        # Validate variable
        if not isinstance(variable, str):
            raise ValidationError("Variable must be a string")
            
        var = symbols(variable)
        
        # Compute definite integral
        result = integrate(expr, (var, lower_bound, upper_bound))
        
        # Try to evaluate numerically if possible
        try:
            numerical_result = float(result.evalf())
            return numerical_result
        except (TypeError, ValueError):
            return result
            
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute definite integral: {str(e)}")


def integrate_indefinite(expression, variable='x'):
    """
    Compute indefinite integral (antiderivative) of an expression.
    
    Args:
        expression (str|sympy.Expr): Mathematical expression to integrate
        variable (str): Variable to integrate with respect to
        
    Returns:
        sympy.Expr: Indefinite integral of the expression
        
    Raises:
        ValidationError: If expression or variable is invalid
        CalculationError: If integration fails
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            try:
                expr = sp.sympify(expression)
            except Exception:
                raise ValidationError(f"Invalid mathematical expression: {expression}")
        else:
            expr = expression
            
        # Validate variable
        if not isinstance(variable, str):
            raise ValidationError("Variable must be a string")
            
        var = symbols(variable)
        
        # Compute indefinite integral
        result = integrate(expr, var)
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute indefinite integral: {str(e)}")


def compute_limit(expression, variable='x', point=0, direction='+'):
    """
    Compute limit of an expression as variable approaches a point.
    
    Args:
        expression (str|sympy.Expr): Mathematical expression
        variable (str): Variable approaching the limit
        point (float|str): Point to approach (can be 'oo' for infinity)
        direction (str): Direction of approach ('+', '-', or '+-')
        
    Returns:
        sympy.Expr|float: Limit value
        
    Raises:
        ValidationError: If expression or parameters are invalid
        CalculationError: If limit calculation fails
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            try:
                expr = sp.sympify(expression)
            except Exception:
                raise ValidationError(f"Invalid mathematical expression: {expression}")
        else:
            expr = expression
            
        # Validate variable
        if not isinstance(variable, str):
            raise ValidationError("Variable must be a string")
            
        var = symbols(variable)
        
        # Parse point
        if isinstance(point, str):
            if point.lower() == 'oo' or point == 'inf':
                point_val = oo
            elif point.lower() == '-oo' or point == '-inf':
                point_val = -oo
            else:
                try:
                    point_val = sp.sympify(point)
                except Exception:
                    raise ValidationError(f"Invalid point: {point}")
        else:
            validate_numbers(point)
            point_val = point
            
        # Validate direction
        if direction not in ['+', '-', '+-']:
            raise ValidationError("Direction must be '+', '-', or '+-'")
            
        # Compute limit
        result = limit(expr, var, point_val, direction)
        
        # Try to evaluate numerically if possible
        try:
            if result.is_real and result.is_finite:
                numerical_result = float(result.evalf())
                return numerical_result
        except (TypeError, ValueError, AttributeError):
            pass
            
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute limit: {str(e)}")


def taylor_series(expression, variable='x', point=0, order=6):
    """
    Compute Taylor series expansion of an expression.
    
    Args:
        expression (str|sympy.Expr): Mathematical expression
        variable (str): Variable for expansion
        point (float): Point around which to expand
        order (int): Order of expansion
        
    Returns:
        sympy.Expr: Taylor series expansion
        
    Raises:
        ValidationError: If expression or parameters are invalid
        CalculationError: If series expansion fails
    """
    try:
        # Validate inputs
        validate_numbers(point)
        if not isinstance(order, int) or order < 0:
            raise ValidationError("Order must be a non-negative integer")
            
        # Parse expression if it's a string
        if isinstance(expression, str):
            try:
                expr = sp.sympify(expression)
            except Exception:
                raise ValidationError(f"Invalid mathematical expression: {expression}")
        else:
            expr = expression
            
        # Validate variable
        if not isinstance(variable, str):
            raise ValidationError("Variable must be a string")
            
        var = symbols(variable)
        
        # Compute Taylor series
        result = series(expr, var, point, order + 1).removeO()
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute Taylor series: {str(e)}")


def partial_derivative(expression, variable='x', order=1):
    """
    Compute partial derivative of a multivariable expression.
    
    Args:
        expression (str|sympy.Expr): Mathematical expression
        variable (str): Variable to differentiate with respect to
        order (int): Order of differentiation
        
    Returns:
        sympy.Expr: Partial derivative
        
    Raises:
        ValidationError: If expression or parameters are invalid
        CalculationError: If differentiation fails
    """
    try:
        # Validate inputs
        if not isinstance(order, int) or order < 1:
            raise ValidationError("Order must be a positive integer")
            
        # Parse expression if it's a string
        if isinstance(expression, str):
            try:
                expr = sp.sympify(expression)
            except Exception:
                raise ValidationError(f"Invalid mathematical expression: {expression}")
        else:
            expr = expression
            
        # Validate variable
        if not isinstance(variable, str):
            raise ValidationError("Variable must be a string")
            
        var = symbols(variable)
        
        # Compute partial derivative
        result = diff(expr, var, order)
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute partial derivative: {str(e)}")


def gradient(expression, variables=['x', 'y']):
    """
    Compute gradient of a multivariable expression.
    
    Args:
        expression (str|sympy.Expr): Mathematical expression
        variables (list): List of variables to compute gradient with respect to
        
    Returns:
        list: List of partial derivatives (gradient components)
        
    Raises:
        ValidationError: If expression or variables are invalid
        CalculationError: If gradient computation fails
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            try:
                expr = sp.sympify(expression)
            except Exception:
                raise ValidationError(f"Invalid mathematical expression: {expression}")
        else:
            expr = expression
            
        # Validate variables
        if not isinstance(variables, list) or len(variables) == 0:
            raise ValidationError("Variables must be a non-empty list")
            
        for var in variables:
            if not isinstance(var, str):
                raise ValidationError("All variables must be strings")
                
        # Compute gradient
        grad = []
        for var_name in variables:
            var = symbols(var_name)
            partial = diff(expr, var)
            grad.append(partial)
            
        return grad
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute gradient: {str(e)}")


def hessian_matrix(expression, variables=['x', 'y']):
    """
    Compute Hessian matrix of a multivariable expression.
    
    Args:
        expression (str|sympy.Expr): Mathematical expression
        variables (list): List of variables
        
    Returns:
        sympy.Matrix: Hessian matrix
        
    Raises:
        ValidationError: If expression or variables are invalid
        CalculationError: If Hessian computation fails
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            try:
                expr = sp.sympify(expression)
            except Exception:
                raise ValidationError(f"Invalid mathematical expression: {expression}")
        else:
            expr = expression
            
        # Validate variables
        if not isinstance(variables, list) or len(variables) == 0:
            raise ValidationError("Variables must be a non-empty list")
            
        for var in variables:
            if not isinstance(var, str):
                raise ValidationError("All variables must be strings")
                
        # Create symbol variables
        var_symbols = [symbols(var) for var in variables]
        
        # Compute Hessian matrix
        n = len(var_symbols)
        hess = sp.Matrix(n, n, lambda i, j: diff(expr, var_symbols[i], var_symbols[j]))
        
        return hess
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute Hessian matrix: {str(e)}")


def numerical_derivative(func, point, h=1e-8):
    """
    Compute numerical derivative using finite differences.
    
    Args:
        func (callable): Function to differentiate
        point (float): Point at which to compute derivative
        h (float): Step size for finite difference
        
    Returns:
        float: Numerical derivative
        
    Raises:
        ValidationError: If inputs are invalid
        CalculationError: If computation fails
    """
    try:
        # Validate inputs
        validate_numbers(point, h)
        if not callable(func):
            raise ValidationError("Function must be callable")
        if h <= 0:
            raise ValidationError("Step size must be positive")
            
        # Compute numerical derivative using central difference
        try:
            f_plus = func(point + h)
            f_minus = func(point - h)
            derivative = (f_plus - f_minus) / (2 * h)
            return derivative
        except Exception:
            # Fall back to forward difference if central difference fails
            f_plus = func(point + h)
            f_point = func(point)
            derivative = (f_plus - f_point) / h
            return derivative
            
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute numerical derivative: {str(e)}")


def numerical_integral(func, lower_bound, upper_bound, method='simpson', n=1000):
    """
    Compute numerical integral using various methods.
    
    Args:
        func (callable): Function to integrate
        lower_bound (float): Lower bound of integration
        upper_bound (float): Upper bound of integration
        method (str): Integration method ('simpson', 'trapezoidal', 'midpoint')
        n (int): Number of intervals
        
    Returns:
        float: Numerical integral value
        
    Raises:
        ValidationError: If inputs are invalid
        CalculationError: If integration fails
    """
    try:
        # Validate inputs
        validate_numbers(lower_bound, upper_bound)
        if not callable(func):
            raise ValidationError("Function must be callable")
        if not isinstance(n, int) or n <= 0:
            raise ValidationError("Number of intervals must be a positive integer")
        if method not in ['simpson', 'trapezoidal', 'midpoint']:
            raise ValidationError("Method must be 'simpson', 'trapezoidal', or 'midpoint'")
            
        # Compute numerical integral
        h = (upper_bound - lower_bound) / n
        
        if method == 'simpson':
            # Simpson's rule
            if n % 2 == 1:
                n += 1  # Ensure n is even for Simpson's rule
                h = (upper_bound - lower_bound) / n
                
            integral = func(lower_bound) + func(upper_bound)
            
            for i in range(1, n):
                x = lower_bound + i * h
                if i % 2 == 0:
                    integral += 2 * func(x)
                else:
                    integral += 4 * func(x)
                    
            integral *= h / 3
            
        elif method == 'trapezoidal':
            # Trapezoidal rule
            integral = (func(lower_bound) + func(upper_bound)) / 2
            
            for i in range(1, n):
                x = lower_bound + i * h
                integral += func(x)
                
            integral *= h
            
        elif method == 'midpoint':
            # Midpoint rule
            integral = 0
            
            for i in range(n):
                x = lower_bound + (i + 0.5) * h
                integral += func(x)
                
            integral *= h
            
        return integral
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute numerical integral: {str(e)}")
