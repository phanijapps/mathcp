"""Symbolic mathematics operations module for advanced mathematical computations.

This module provides comprehensive symbolic mathematics capabilities including expression parsing,
manipulation, solving, differentiation, integration, and series expansion.

Example usage:
    >>> from mathgenius.advanced.symbolic import parse_expression, expand_expression, symbolic_integrate
    >>> parse_expression("x^2 + 3*x + 2")
    x**2 + 3*x + 2
    >>> expand_expression("(x + 1)*(x + 2)")
    x**2 + 3*x + 2
    >>> symbolic_integrate("x^2", "x")
    x**3/3
"""

import sympy as sp
from sympy import symbols, sympify, expand, factor, simplify, collect, solve, dsolve
from sympy import latex, pprint, pretty, Rational, oo, I, pi, E
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from sympy.solvers import solve as sympy_solve
from sympy.solvers.ode import dsolve as sympy_dsolve
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError


def _parse_expression_with_transformations(expression_string):
    """
    Parse a mathematical expression string with common transformations.
    
    This function handles common mathematical notation like:
    - ^ for exponentiation (converts to **)
    - Implicit multiplication
    - Standard mathematical transformations
    
    Args:
        expression_string (str): Mathematical expression as string
        
    Returns:
        sympy.Expr: Parsed SymPy expression
        
    Raises:
        Exception: If parsing fails
    """
    # First, try to handle ^ operator by replacing with **
    # This is a simple preprocessing step
    processed_expr = expression_string.replace('^', '**')
    
    # Use SymPy's transformations for better parsing
    transformations = (standard_transformations + 
                      (implicit_multiplication_application,))
    
    try:
        # Try with transformations first
        expr = parse_expr(processed_expr, transformations=transformations)
        return expr
    except Exception:
        # Fallback to basic parsing
        expr = parse_expr(processed_expr)
        return expr


def parse_expression(expression_string):
    """
    Parse a mathematical expression string into a SymPy expression.
    
    Args:
        expression_string (str): Mathematical expression as string
        
    Returns:
        str: Parsed expression as string
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If parsing fails
    
    Examples:
        >>> parse_expression("x^2 + 3*x + 2")
        'x**2 + 3*x + 2'
        >>> parse_expression("sin(x) + cos(x)")
        'sin(x) + cos(x)'
        >>> parse_expression("exp(x) * log(x)")
        'exp(x)*log(x)'
    """
    try:
        # Validate input
        if not isinstance(expression_string, str):
            raise ValidationError("Expression must be a string")
        if not expression_string.strip():
            raise ValidationError("Expression cannot be empty")
            
        # Parse expression with transformations to handle ^ operator
        expr = _parse_expression_with_transformations(expression_string)
        return str(expr)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to parse expression: {str(e)}")


def create_symbol(symbol_name, assumptions=None):
    """
    Create a symbolic variable with optional assumptions.
    
    Args:
        symbol_name (str): Name of the symbol
        assumptions (dict): Dictionary of assumptions (e.g., {'real': True, 'positive': True})
        
    Returns:
        str: Symbol name as string
        
    Raises:
        ValidationError: If symbol name is invalid
        CalculationError: If symbol creation fails
    
    Examples:
        >>> create_symbol("x")
        'x'
        >>> create_symbol("y", {"real": True})
        'y'
        >>> create_symbol("z", {"positive": True, "integer": True})
        'z'
    """
    try:
        # Validate input
        if not isinstance(symbol_name, str):
            raise ValidationError("Symbol name must be a string")
        if not symbol_name.strip():
            raise ValidationError("Symbol name cannot be empty")
            
        # Create symbol with assumptions
        if assumptions is None:
            symbol = symbols(symbol_name)
        else:
            symbol = symbols(symbol_name, **assumptions)
            
        return str(symbol)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to create symbol: {str(e)}")


def expand_expression(expression):
    """
    Expand a mathematical expression.
    
    Args:
        expression (str): Expression to expand as string
        
    Returns:
        str: Expanded expression as string
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If expansion fails
    
    Examples:
        >>> expand_expression("(x + 1)*(x + 2)")
        'x**2 + 3*x + 2'
        >>> expand_expression("(a + b)**2")
        'a**2 + 2*a*b + b**2'
        >>> expand_expression("sin(x + y)")
        'sin(x)*cos(y) + cos(x)*sin(y)'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = _parse_expression_with_transformations(expression)
        else:
            expr = expression
            
        # Expand expression
        result = expand(expr)
        
        # Convert to string for JSON serialization
        return str(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to expand expression: {str(e)}")


def factor_expression(expression):
    """
    Factor a mathematical expression.
    
    Args:
        expression (str): Expression to factor as string
        
    Returns:
        str: Factored expression as string
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If factoring fails
    
    Examples:
        >>> factor_expression("x^2 + 3*x + 2")
        '(x + 1)*(x + 2)'
        >>> factor_expression("x^2 - 4")
        '(x - 2)*(x + 2)'
        >>> factor_expression("x^3 - 1")
        '(x - 1)*(x**2 + x + 1)'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = _parse_expression_with_transformations(expression)
        else:
            expr = expression
            
        # Factor expression
        result = factor(expr)
        
        # Convert to string for JSON serialization
        return str(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to factor expression: {str(e)}")


def simplify_expression(expression):
    """
    Simplify a mathematical expression.
    
    Args:
        expression (str): Expression to simplify as string
        
    Returns:
        str: Simplified expression as string
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If simplification fails
    
    Examples:
        >>> simplify_expression("x^2 + 2*x + 1")
        'x**2 + 2*x + 1'
        >>> simplify_expression("sin(x)^2 + cos(x)^2")
        '1'
        >>> simplify_expression("(x^2 - 1)/(x - 1)")
        'x + 1'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = _parse_expression_with_transformations(expression)
        else:
            expr = expression
            
        # Simplify expression
        result = simplify(expr)
        
        # Convert to string for JSON serialization
        return str(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to simplify expression: {str(e)}")


def collect_terms(expression, variable):
    """
    Collect terms with respect to a variable.
    
    Args:
        expression (str): Expression to collect terms from as string
        variable (str): Variable to collect terms for
        
    Returns:
        str: Expression with collected terms as string
        
    Raises:
        ValidationError: If expression or variable is invalid
        CalculationError: If collection fails
    
    Examples:
        >>> collect_terms("x^2 + 2*x + 3*x + 1", "x")
        'x**2 + 5*x + 1'
        >>> collect_terms("a*x + b*x + c", "x")
        '(a + b)*x + c'
        >>> collect_terms("x*y + x*z + y*z", "x")
        'x*(y + z) + y*z'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Parse variable if it's a string
        if isinstance(variable, str):
            var = symbols(variable)
        elif isinstance(variable, sp.Symbol):
            var = variable
        else:
            raise ValidationError("Variable must be a string or SymPy symbol")
            
        # Collect terms
        result = collect(expr, var)
        return str(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to collect terms: {str(e)}")


def solve_equation(equation, variable=None):
    """
    Solve an equation or system of equations.
    
    Args:
        equation (str): Equation(s) to solve as string
        variable (str): Variable(s) to solve for
        
    Returns:
        list: List of solutions as strings
        
    Raises:
        ValidationError: If equation or variable is invalid
        CalculationError: If solving fails
    
    Examples:
        >>> solve_equation("x^2 - 5*x + 6 = 0")
        ['2', '3']
        >>> solve_equation("x^2 - 4 = 0", "x")
        ['-2', '2']
        >>> solve_equation("sin(x) = 0.5", "x")
        ['0.523598775598299', '2.61799387799149']
        >>> solve_equation("exp(x) = 10", "x")
        ['2.30258509299405']
    """
    try:
        # Parse equation if it's a string
        if isinstance(equation, str):
            eq = parse_expr(equation)
        elif isinstance(equation, list):
            eq = [parse_expr(e) if isinstance(e, str) else e for e in equation]
        else:
            eq = equation
            
        # Parse variable if it's a string
        if variable is None:
            var = None
        elif isinstance(variable, str):
            var = symbols(variable)
        elif isinstance(variable, list):
            var = [symbols(v) if isinstance(v, str) else v for v in variable]
        else:
            var = variable
            
        # Solve equation
        solutions = sympy_solve(eq, var)
        
        # Convert solutions to list format and string for JSON serialization
        if isinstance(solutions, dict):
            return [str(solutions)]
        elif isinstance(solutions, list):
            return [str(sol) for sol in solutions]
        else:
            return [str(solutions)]
            
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to solve equation: {str(e)}")


def solve_differential_equation(equation, function=None):
    """
    Solve a differential equation.
    
    Args:
        equation (str): Differential equation to solve as string
        function (str): Function to solve for
        
    Returns:
        str: General solution of the differential equation
        
    Raises:
        ValidationError: If equation or function is invalid
        CalculationError: If solving fails
    
    Examples:
        >>> solve_differential_equation("diff(y(x), x) - y(x) = 0")
        'C1*exp(x)'
        >>> solve_differential_equation("diff(y(x), x, 2) + y(x) = 0")
        'C1*sin(x) + C2*cos(x)'
        >>> solve_differential_equation("diff(y(x), x) + 2*y(x) = 0")
        'C1*exp(-2*x)'
    """
    try:
        # Parse equation if it's a string
        if isinstance(equation, str):
            eq = parse_expr(equation)
        else:
            eq = equation
            
        # Parse function if it's a string
        if function is None:
            func = None
        elif isinstance(function, str):
            # Create a function symbol like y(x)
            x = symbols('x')
            func = sp.Function(function)(x)
        else:
            func = function
            
        # Solve differential equation
        solution = sympy_dsolve(eq, func)
        return str(solution)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to solve differential equation: {str(e)}")


def substitute_expression(expression, substitutions):
    """
    Substitute values or expressions into an expression.
    
    Args:
        expression (str): Expression to substitute into as string
        substitutions (dict): Dictionary of substitutions {variable: value}
        
    Returns:
        str: Expression with substitutions applied as string
        
    Raises:
        ValidationError: If expression or substitutions are invalid
        CalculationError: If substitution fails
    
    Examples:
        >>> substitute_expression("x^2 + y^2", {"x": 2, "y": 3})
        '13'
        >>> substitute_expression("sin(x)", {"x": "pi/2"})
        '1'
        >>> substitute_expression("a*x + b", {"a": 2, "b": 5, "x": 3})
        '11'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Validate substitutions
        if not isinstance(substitutions, dict):
            raise ValidationError("Substitutions must be a dictionary")
            
        # Convert string variables to symbols
        sub_dict = {}
        for var, value in substitutions.items():
            if isinstance(var, str):
                var_symbol = symbols(var)
            else:
                var_symbol = var
                
            if isinstance(value, str):
                value_expr = parse_expr(value)
            else:
                value_expr = value
                
            sub_dict[var_symbol] = value_expr
            
        # Perform substitution
        result = expr.subs(sub_dict)
        return str(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to substitute expression: {str(e)}")


def evaluate_expression(expression, substitutions=None):
    """
    Evaluate an expression numerically.
    
    Args:
        expression (str): Expression to evaluate as string
        substitutions (dict): Dictionary of variable values
        
    Returns:
        float|complex: Numerical value of the expression
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If evaluation fails
    
    Examples:
        >>> evaluate_expression("x^2 + 2*x + 1", {"x": 2})
        9.0
        >>> evaluate_expression("sin(pi/2)")
        1.0
        >>> evaluate_expression("exp(1)")
        2.718281828459045
        >>> evaluate_expression("sqrt(16)")
        4.0
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Apply substitutions if provided
        if substitutions is not None:
            expr = substitute_expression(expr, substitutions)
            
        # Evaluate expression numerically
        result = expr.evalf()
        
        # Try to convert to Python numeric type
        try:
            if result.is_real:
                return float(result)
            else:
                return complex(result)
        except (TypeError, ValueError):
            return result
            
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to evaluate expression: {str(e)}")


def expression_to_latex(expression):
    """
    Convert an expression to LaTeX format.
    
    Args:
        expression (str): Expression to convert as string
        
    Returns:
        str: LaTeX representation of the expression
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If conversion fails
    
    Examples:
        >>> expression_to_latex("x^2 + 3*x + 2")
        'x^{2} + 3 x + 2'
        >>> expression_to_latex("sin(x) + cos(x)")
        '\\sin{\\left(x \\right)} + \\cos{\\left(x \\right)}'
        >>> expression_to_latex("frac(1, 2)")
        '\\frac{1}{2}'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Convert to LaTeX
        latex_str = latex(expr)
        return latex_str
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to convert to LaTeX: {str(e)}")


def expression_to_string(expression, pretty_print=False):
    """
    Convert an expression to string format.
    
    Args:
        expression (str): Expression to convert as string
        pretty_print (bool): Whether to use pretty printing
        
    Returns:
        str: String representation of the expression
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If conversion fails
    
    Examples:
        >>> expression_to_string("x^2 + 3*x + 2")
        'x**2 + 3*x + 2'
        >>> expression_to_string("sin(x) + cos(x)")
        'sin(x) + cos(x)'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Convert to string
        if pretty_print:
            result = pretty(expr)
        else:
            result = str(expr)
            
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to convert to string: {str(e)}")


def symbolic_integrate(expression, variable, limits=None):
    """
    Perform symbolic integration.
    
    Args:
        expression (str): Expression to integrate as string
        variable (str): Variable to integrate with respect to
        limits (tuple): Integration limits (lower, upper) for definite integral
        
    Returns:
        str: Integrated expression as string
        
    Raises:
        ValidationError: If expression or variable is invalid
        CalculationError: If integration fails
    
    Examples:
        >>> symbolic_integrate("x^2", "x")
        'x**3/3'
        >>> symbolic_integrate("sin(x)", "x")
        '-cos(x)'
        >>> symbolic_integrate("x^2", "x", (0, 1))
        '1/3'
        >>> symbolic_integrate("exp(x)", "x")
        'exp(x)'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Parse variable if it's a string
        if isinstance(variable, str):
            var = symbols(variable)
        else:
            var = variable
            
        # Perform integration
        if limits is None:
            # Indefinite integral
            result = sp.integrate(expr, var)
        else:
            # Definite integral
            if len(limits) != 2:
                raise ValidationError("Limits must be a tuple of two values")
            lower, upper = limits
            result = sp.integrate(expr, (var, lower, upper))
            
        return str(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to integrate symbolically: {str(e)}")


def symbolic_differentiate(expression, variable, order=1):
    """
    Perform symbolic differentiation.
    
    Args:
        expression (str): Expression to differentiate as string
        variable (str): Variable to differentiate with respect to
        order (int): Order of differentiation
        
    Returns:
        str: Differentiated expression as string
        
    Raises:
        ValidationError: If expression, variable, or order is invalid
        CalculationError: If differentiation fails
    
    Examples:
        >>> symbolic_differentiate("x^3", "x")
        '3*x**2'
        >>> symbolic_differentiate("sin(x)", "x")
        'cos(x)'
        >>> symbolic_differentiate("exp(x)", "x")
        'exp(x)'
        >>> symbolic_differentiate("x^3", "x", 2)
        '6*x'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Parse variable if it's a string
        if isinstance(variable, str):
            var = symbols(variable)
        else:
            var = variable
            
        # Validate order
        if not isinstance(order, int) or order < 1:
            raise ValidationError("Order must be a positive integer")
            
        # Perform differentiation
        result = sp.diff(expr, var, order)
        return str(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to differentiate symbolically: {str(e)}")


def symbolic_limit(expression, variable, point, direction='+'):
    """
    Compute symbolic limit.
    
    Args:
        expression (str): Expression to find limit of as string
        variable (str): Variable approaching the limit
        point (str|number): Point to approach
        direction (str): Direction of approach ('+', '-', or '+-')
        
    Returns:
        str: Limit value as string
        
    Raises:
        ValidationError: If expression, variable, or parameters are invalid
        CalculationError: If limit computation fails
    
    Examples:
        >>> symbolic_limit("sin(x)/x", "x", 0)
        '1'
        >>> symbolic_limit("(1 + 1/x)^x", "x", "oo")
        'E'
        >>> symbolic_limit("1/x", "x", 0, "+")
        'oo'
        >>> symbolic_limit("1/x", "x", 0, "-")
        '-oo'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Parse variable if it's a string
        if isinstance(variable, str):
            var = symbols(variable)
        else:
            var = variable
            
        # Parse point
        if isinstance(point, str):
            if point.lower() in ['oo', 'inf', 'infinity']:
                point_val = oo
            elif point.lower() in ['-oo', '-inf', '-infinity']:
                point_val = -oo
            else:
                point_val = parse_expr(point)
        else:
            point_val = point
            
        # Validate direction
        if direction not in ['+', '-', '+-']:
            raise ValidationError("Direction must be '+', '-', or '+-'")
            
        # Compute limit
        result = sp.limit(expr, var, point_val, direction)
        return str(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute symbolic limit: {str(e)}")


def symbolic_series(expression, variable, point=0, order=6):
    """
    Compute symbolic series expansion.
    
    Args:
        expression (str): Expression to expand as string
        variable (str): Variable for expansion
        point (number): Point around which to expand
        order (int): Order of expansion
        
    Returns:
        str: Series expansion as string
        
    Raises:
        ValidationError: If expression, variable, or parameters are invalid
        CalculationError: If series computation fails
    
    Examples:
        >>> symbolic_series("exp(x)", "x", 0, 3)
        '1 + x + x**2/2 + x**3/6'
        >>> symbolic_series("sin(x)", "x", 0, 5)
        'x - x**3/6 + x**5/120'
        >>> symbolic_series("cos(x)", "x", 0, 4)
        '1 - x**2/2 + x**4/24'
        >>> symbolic_series("1/(1 - x)", "x", 0, 3)
        '1 + x + x**2 + x**3'
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Parse variable if it's a string
        if isinstance(variable, str):
            var = symbols(variable)
        else:
            var = variable
            
        # Validate parameters
        if not isinstance(order, int) or order < 0:
            raise ValidationError("Order must be a non-negative integer")
            
        # Compute series
        result = sp.series(expr, var, point, order + 1).removeO()
        return str(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute symbolic series: {str(e)}")


def create_rational(numerator, denominator):
    """
    Create a rational number (fraction).
    
    Args:
        numerator (int): Numerator
        denominator (int): Denominator
        
    Returns:
        str: Rational number as string
        
    Raises:
        ValidationError: If inputs are invalid
        CalculationError: If creation fails
    
    Examples:
        >>> create_rational(1, 2)
        '1/2'
        >>> create_rational(3, 4)
        '3/4'
        >>> create_rational(5, 1)
        '5'
        >>> create_rational(0, 1)
        '0'
    """
    try:
        # Validate inputs
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise ValidationError("Numerator and denominator must be integers")
        if denominator == 0:
            raise ValidationError("Denominator cannot be zero")
            
        # Create rational number
        result = Rational(numerator, denominator)
        return str(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to create rational number: {str(e)}")


def is_polynomial(expression, variable=None):
    """
    Check if an expression is a polynomial.
    
    Args:
        expression (str): Expression to check as string
        variable (str): Variable to check polynomial in
        
    Returns:
        bool: True if expression is a polynomial
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If check fails
    
    Examples:
        >>> is_polynomial("x^2 + 3*x + 2")
        True
        >>> is_polynomial("sin(x) + 1")
        False
        >>> is_polynomial("x^2 + 1/x")
        False
        >>> is_polynomial("x^2 + y^2", "x")
        True
        >>> is_polynomial("exp(x)")
        False
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Parse variable if it's a string
        if variable is None:
            var = None
        elif isinstance(variable, str):
            var = symbols(variable)
        else:
            var = variable
            
        # Check if polynomial
        if var is None:
            # Check if polynomial in any variable
            free_vars = expr.free_symbols
            if len(free_vars) == 0:
                return True
            elif len(free_vars) == 1:
                var = list(free_vars)[0]
                result = expr.is_polynomial(var)
                return result if result is not None else False
            else:
                # Multiple variables - check if polynomial in all
                results = [expr.is_polynomial(v) for v in free_vars]
                return all(r if r is not None else False for r in results)
        else:
            result = expr.is_polynomial(var)
            return result if result is not None else False
            
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to check if polynomial: {str(e)}")
