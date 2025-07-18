"""Symbolic mathematics operations module for advanced mathematical computations."""
import sympy as sp
from sympy import symbols, sympify, expand, factor, simplify, collect, solve, dsolve
from sympy import latex, pprint, pretty, Rational, oo, I, pi, E
from sympy.parsing.sympy_parser import parse_expr
from sympy.solvers import solve as sympy_solve
from sympy.solvers.ode import dsolve as sympy_dsolve
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError


def parse_expression(expression_string):
    """
    Parse a mathematical expression string into a SymPy expression.
    
    Args:
        expression_string (str): Mathematical expression as string
        
    Returns:
        sympy.Expr: Parsed SymPy expression
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If parsing fails
    """
    try:
        # Validate input
        if not isinstance(expression_string, str):
            raise ValidationError("Expression must be a string")
        if not expression_string.strip():
            raise ValidationError("Expression cannot be empty")
            
        # Parse expression
        expr = parse_expr(expression_string)
        return expr
        
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
        sympy.Symbol: Created symbol
        
    Raises:
        ValidationError: If symbol name is invalid
        CalculationError: If symbol creation fails
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
            
        return symbol
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to create symbol: {str(e)}")


def expand_expression(expression):
    """
    Expand a mathematical expression.
    
    Args:
        expression (str|sympy.Expr): Expression to expand
        
    Returns:
        sympy.Expr: Expanded expression
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If expansion fails
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Expand expression
        result = expand(expr)
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to expand expression: {str(e)}")


def factor_expression(expression):
    """
    Factor a mathematical expression.
    
    Args:
        expression (str|sympy.Expr): Expression to factor
        
    Returns:
        sympy.Expr: Factored expression
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If factoring fails
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Factor expression
        result = factor(expr)
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to factor expression: {str(e)}")


def simplify_expression(expression):
    """
    Simplify a mathematical expression.
    
    Args:
        expression (str|sympy.Expr): Expression to simplify
        
    Returns:
        sympy.Expr: Simplified expression
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If simplification fails
    """
    try:
        # Parse expression if it's a string
        if isinstance(expression, str):
            expr = parse_expr(expression)
        else:
            expr = expression
            
        # Simplify expression
        result = simplify(expr)
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to simplify expression: {str(e)}")


def collect_terms(expression, variable):
    """
    Collect terms with respect to a variable.
    
    Args:
        expression (str|sympy.Expr): Expression to collect terms from
        variable (str|sympy.Symbol): Variable to collect terms for
        
    Returns:
        sympy.Expr: Expression with collected terms
        
    Raises:
        ValidationError: If expression or variable is invalid
        CalculationError: If collection fails
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
            
        # Collect terms
        result = collect(expr, var)
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to collect terms: {str(e)}")


def solve_equation(equation, variable=None):
    """
    Solve an equation or system of equations.
    
    Args:
        equation (str|sympy.Expr|list): Equation(s) to solve
        variable (str|sympy.Symbol|list): Variable(s) to solve for
        
    Returns:
        list: List of solutions
        
    Raises:
        ValidationError: If equation or variable is invalid
        CalculationError: If solving fails
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
        
        # Convert solutions to list format
        if isinstance(solutions, dict):
            return [solutions]
        elif isinstance(solutions, list):
            return solutions
        else:
            return [solutions]
            
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to solve equation: {str(e)}")


def solve_differential_equation(equation, function=None):
    """
    Solve a differential equation.
    
    Args:
        equation (str|sympy.Expr): Differential equation to solve
        function (str|sympy.Function): Function to solve for
        
    Returns:
        sympy.Expr: General solution of the differential equation
        
    Raises:
        ValidationError: If equation or function is invalid
        CalculationError: If solving fails
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
            func = sp.Function(function)
        else:
            func = function
            
        # Solve differential equation
        solution = sympy_dsolve(eq, func)
        return solution
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to solve differential equation: {str(e)}")


def substitute_expression(expression, substitutions):
    """
    Substitute values or expressions into an expression.
    
    Args:
        expression (str|sympy.Expr): Expression to substitute into
        substitutions (dict): Dictionary of substitutions {variable: value}
        
    Returns:
        sympy.Expr: Expression with substitutions applied
        
    Raises:
        ValidationError: If expression or substitutions are invalid
        CalculationError: If substitution fails
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
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to substitute expression: {str(e)}")


def evaluate_expression(expression, substitutions=None):
    """
    Evaluate an expression numerically.
    
    Args:
        expression (str|sympy.Expr): Expression to evaluate
        substitutions (dict): Dictionary of variable values
        
    Returns:
        float|complex: Numerical value of the expression
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If evaluation fails
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
        expression (str|sympy.Expr): Expression to convert
        
    Returns:
        str: LaTeX representation of the expression
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If conversion fails
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
        expression (str|sympy.Expr): Expression to convert
        pretty_print (bool): Whether to use pretty printing
        
    Returns:
        str: String representation of the expression
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If conversion fails
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
        expression (str|sympy.Expr): Expression to integrate
        variable (str|sympy.Symbol): Variable to integrate with respect to
        limits (tuple): Integration limits (lower, upper) for definite integral
        
    Returns:
        sympy.Expr: Integrated expression
        
    Raises:
        ValidationError: If expression or variable is invalid
        CalculationError: If integration fails
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
            
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to integrate symbolically: {str(e)}")


def symbolic_differentiate(expression, variable, order=1):
    """
    Perform symbolic differentiation.
    
    Args:
        expression (str|sympy.Expr): Expression to differentiate
        variable (str|sympy.Symbol): Variable to differentiate with respect to
        order (int): Order of differentiation
        
    Returns:
        sympy.Expr: Differentiated expression
        
    Raises:
        ValidationError: If expression, variable, or order is invalid
        CalculationError: If differentiation fails
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
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to differentiate symbolically: {str(e)}")


def symbolic_limit(expression, variable, point, direction='+'):
    """
    Compute symbolic limit.
    
    Args:
        expression (str|sympy.Expr): Expression to find limit of
        variable (str|sympy.Symbol): Variable approaching the limit
        point (str|number): Point to approach
        direction (str): Direction of approach ('+', '-', or '+-')
        
    Returns:
        sympy.Expr: Limit value
        
    Raises:
        ValidationError: If expression, variable, or parameters are invalid
        CalculationError: If limit computation fails
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
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute symbolic limit: {str(e)}")


def symbolic_series(expression, variable, point=0, order=6):
    """
    Compute symbolic series expansion.
    
    Args:
        expression (str|sympy.Expr): Expression to expand
        variable (str|sympy.Symbol): Variable for expansion
        point (number): Point around which to expand
        order (int): Order of expansion
        
    Returns:
        sympy.Expr: Series expansion
        
    Raises:
        ValidationError: If expression, variable, or parameters are invalid
        CalculationError: If series computation fails
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
        return result
        
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
        sympy.Rational: Rational number
        
    Raises:
        ValidationError: If inputs are invalid
        CalculationError: If creation fails
    """
    try:
        # Validate inputs
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise ValidationError("Numerator and denominator must be integers")
        if denominator == 0:
            raise ValidationError("Denominator cannot be zero")
            
        # Create rational number
        result = Rational(numerator, denominator)
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to create rational number: {str(e)}")


def is_polynomial(expression, variable=None):
    """
    Check if an expression is a polynomial.
    
    Args:
        expression (str|sympy.Expr): Expression to check
        variable (str|sympy.Symbol): Variable to check polynomial in
        
    Returns:
        bool: True if expression is a polynomial
        
    Raises:
        ValidationError: If expression is invalid
        CalculationError: If check fails
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
                return expr.is_polynomial(var)
            else:
                # Multiple variables - check if polynomial in all
                return all(expr.is_polynomial(v) for v in free_vars)
        else:
            return expr.is_polynomial(var)
            
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to check if polynomial: {str(e)}")
