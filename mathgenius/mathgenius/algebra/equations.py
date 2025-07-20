"""Equation solving functions for mathgenius.

This module provides comprehensive equation solving capabilities including linear, quadratic, cubic,
and general equation solving using symbolic mathematics.

Example usage:
    >>> from mathgenius.algebra.equations import solve_linear, solve_quadratic, solve_equation
    >>> solve_linear(2, -4)  # Solve 2x - 4 = 0
    2.0
    >>> solve_quadratic(1, -5, 6)  # Solve x² - 5x + 6 = 0
    [2.0, 3.0]
    >>> solve_equation("x^3 - 6*x^2 + 11*x - 6 = 0")
    [1.0, 2.0, 3.0]
"""

from sympy import symbols, Eq, solve, sympify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError


def solve_linear(a, b):
    """
    Solve a linear equation of the form ax + b = 0.
    
    Args:
        a (float): Coefficient of x (must be non-zero)
        b (float): Constant term
    
    Returns:
        float: The solution x = -b/a
    
    Raises:
        ValidationError: If inputs are invalid or a is zero
    
    Examples:
        >>> solve_linear(2, -4)
        2.0
        >>> solve_linear(3, 6)
        -2.0
        >>> solve_linear(1, 0)
        0.0
    """
    try:
        validate_numbers(a, b)
        if a == 0:
            raise ValidationError("Coefficient 'a' cannot be zero for linear equation")
            
        x = symbols('x')
        eq = Eq(a * x + b, 0)
        solutions = solve(eq, x)
        
        if not solutions:
            return None
            
        sol = solutions[0]
        try:
            # Try to convert to float if it's a real number
            float_val = float(sol.evalf())
            if abs(float_val - float(sol)) < 1e-10:
                return float_val
            else:
                return str(sol)  # Convert to string for JSON serialization
        except:
            return str(sol)  # Fallback to string representation
            
    except Exception as e:
        raise ValidationError(str(e))


def solve_quadratic(a, b, c):
    """
    Solve a quadratic equation of the form ax² + bx + c = 0.
    
    Args:
        a (float): Coefficient of x² (must be non-zero)
        b (float): Coefficient of x
        c (float): Constant term
    
    Returns:
        list: List of solutions (can be 0, 1, or 2 solutions)
    
    Raises:
        ValidationError: If inputs are invalid or a is zero
    
    Examples:
        >>> solve_quadratic(1, -5, 6)  # x² - 5x + 6 = 0
        [2.0, 3.0]
        >>> solve_quadratic(1, 0, -4)  # x² - 4 = 0
        [-2.0, 2.0]
        >>> solve_quadratic(1, 2, 1)  # x² + 2x + 1 = 0
        [-1.0]
        >>> solve_quadratic(1, 0, 1)  # x² + 1 = 0 (complex roots)
        ['-I', 'I']
    """
    try:
        validate_numbers(a, b, c)
        if a == 0:
            raise ValidationError("Coefficient 'a' cannot be zero for quadratic equation")
            
        x = symbols('x')
        eq = Eq(a * x**2 + b * x + c, 0)
        solutions = solve(eq, x)
        
        # Convert solutions to float when possible for better JSON serialization
        result = []
        for sol in solutions:
            try:
                # Try to convert to float if it's a real number
                float_val = float(sol.evalf())
                if abs(float_val - float(sol)) < 1e-10:  # Check if it's essentially the same
                    result.append(float_val)
                else:
                    result.append(str(sol))  # Convert to string for JSON serialization
            except:
                result.append(str(sol))  # Fallback to string representation
        
        return result
    except Exception as e:
        raise ValidationError(str(e))


def solve_equation(equation_str, variable='x'):
    """
    Solve a general equation given as a string.
    
    This function can handle various types of equations including polynomial, 
    trigonometric, exponential, and logarithmic equations. It uses SymPy's
    symbolic solving capabilities.
    
    Args:
        equation_str (str): The equation to solve as a string.
                           Examples: "x^2 - 5*x + 6 = 0", "sin(x) = 0.5", "exp(x) = 10"
        variable (str): The variable to solve for (default: 'x')
    
    Returns:
        list: List of solutions. Solutions are returned as floats when possible,
              or as strings for complex or symbolic solutions.
    
    Raises:
        ValidationError: If the equation cannot be parsed or solved
    
    Examples:
        >>> solve_equation("x^2 - 5*x + 6 = 0")
        [2.0, 3.0]
        >>> solve_equation("2*x + 3 = 7")
        [2.0]
        >>> solve_equation("x^3 - 6*x^2 + 11*x - 6 = 0")
        [1.0, 2.0, 3.0]
        >>> solve_equation("sin(x) = 0.5")
        [0.523598775598299, 2.61799387799149]
        >>> solve_equation("exp(x) = 10")
        [2.30258509299405]
    """
    try:
        # Create symbolic variable
        var = symbols(variable)
        
        # Handle equation parsing more robustly
        try:
            # First, handle the equation string properly
            equation_str = str(equation_str).strip()
            
            # Split equation on '=' sign
            if '=' in equation_str:
                left_side, right_side = equation_str.split('=', 1)
                left_side = left_side.strip()
                right_side = right_side.strip()
            else:
                # If no '=' sign, assume the expression equals zero
                left_side = equation_str
                right_side = '0'
            
            # Replace ^ with ** for proper Python/SymPy syntax
            left_side = left_side.replace('^', '**')
            right_side = right_side.replace('^', '**')
            
            # Parse both sides with proper transformations
            transformations = (standard_transformations + 
                              (implicit_multiplication_application,))
            
            # Use a more robust parsing approach
            try:
                left_expr = parse_expr(left_side, transformations=transformations)
                right_expr = parse_expr(right_side, transformations=transformations)
            except Exception as parse_error:
                # Fallback to sympify if parse_expr fails
                left_expr = sympify(left_side)
                right_expr = sympify(right_side)
            
            # Create equation object
            eq = Eq(left_expr, right_expr)
            
            # Solve the equation
            solutions = solve(eq, var)
            
        except Exception as e:
            # Provide more detailed error information
            raise ValidationError(f"Failed to solve equation: {str(e)}")
        
        # Convert solutions to float when possible for better readability
        result = []
        for sol in solutions:
            try:
                # Check if solution is purely numeric (no variables)
                if sol.is_number:
                    # Try to convert to float if it's a real number
                    float_val = float(sol.evalf())
                    if abs(float_val - float(sol)) < 1e-10:  # Check if it's essentially the same
                        result.append(float_val)
                    else:
                        result.append(str(sol))  # Convert to string for JSON serialization
                else:
                    # Solution contains variables, convert to string
                    result.append(str(sol))
            except:
                result.append(str(sol))  # Fallback to string representation
        
        return result
        
    except Exception as e:
        raise ValidationError(f"Failed to solve equation: {str(e)}")


def solve_cubic(a, b, c, d):
    """
    Solve a cubic equation of the form ax³ + bx² + cx + d = 0.
    
    Args:
        a (float): Coefficient of x³ (must be non-zero)
        b (float): Coefficient of x²
        c (float): Coefficient of x
        d (float): Constant term
    
    Returns:
        list: List of solutions (can be 1, 2, or 3 solutions)
    
    Raises:
        ValidationError: If inputs are invalid or a is zero
    
    Examples:
        >>> solve_cubic(1, -6, 11, -6)  # x³ - 6x² + 11x - 6 = 0
        [1.0, 2.0, 3.0]
        >>> solve_cubic(1, 0, -7, 6)  # x³ - 7x + 6 = 0
        [-3.0, 1.0, 2.0]
        >>> solve_cubic(1, 0, 0, -8)  # x³ - 8 = 0
        [2.0, -1.0 - 1.73205080756888*I, -1.0 + 1.73205080756888*I]
    """
    try:
        validate_numbers(a, b, c, d)
        if a == 0:
            raise ValidationError("Coefficient 'a' cannot be zero for cubic equation")
        
        x = symbols('x')
        eq = Eq(a * x**3 + b * x**2 + c * x + d, 0)
        solutions = solve(eq, x)
        
        # Convert to float when possible
        result = []
        for sol in solutions:
            try:
                float_val = float(sol.evalf())
                if abs(float_val - float(sol)) < 1e-10:
                    result.append(float_val)
                else:
                    result.append(str(sol))  # Convert to string for JSON serialization
            except:
                result.append(str(sol))  # Fallback to string representation
        
        return result
        
    except Exception as e:
        raise ValidationError(str(e))
