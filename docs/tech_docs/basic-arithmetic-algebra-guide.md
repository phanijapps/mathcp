# Basic Arithmetic & Algebra Documentation

## Overview

The Math Genius library provides foundational arithmetic and algebra functionality, implementing all requirements from Story 1. This documentation covers basic mathematical operations, equation solving, and polynomial manipulation with comprehensive examples and API reference.

## Quick Start

```python
from mathgenius.api.dispatcher import (
    # Arithmetic operations
    add, subtract, multiply, divide, power, modulo,
    # Algebra functions
    solve_linear, solve_quadratic,
    expand_expr, factor_expr, simplify_expr
)

# Basic arithmetic examples
sum_result = add(5, 3)  # 8
difference = subtract(10, 4)  # 6
product = multiply(7, 6)  # 42
quotient = divide(15, 3)  # 5.0

# Algebra examples
linear_solution = solve_linear(2, -6)  # x = 3 (solving 2x - 6 = 0)
quadratic_solutions = solve_quadratic(1, -5, 6)  # [2, 3] (solving x² - 5x + 6 = 0)
```

## Arithmetic Operations

### Basic Operations

The library provides six fundamental arithmetic operations with robust error handling:

#### Addition

```python
# Basic addition
result = add(5, 3)  # 8
result = add(-2, 7)  # 5
result = add(3.14, 2.86)  # 6.0

# With decimal numbers
result = add(0.1, 0.2)  # 0.30000000000000004 (floating point precision)
```

#### Subtraction

```python
# Basic subtraction
result = subtract(10, 4)  # 6
result = subtract(3, 8)  # -5
result = subtract(15.5, 3.2)  # 12.3

# Negative numbers
result = subtract(-5, -3)  # -2
result = subtract(-2, 3)  # -5
```

#### Multiplication

```python
# Basic multiplication
result = multiply(6, 7)  # 42
result = multiply(-3, 4)  # -12
result = multiply(2.5, 4)  # 10.0

# Zero multiplication
result = multiply(0, 100)  # 0
result = multiply(-5, 0)  # 0
```

#### Division

```python
# Basic division
result = divide(15, 3)  # 5.0
result = divide(7, 2)  # 3.5
result = divide(-12, 4)  # -3.0

# Decimal division
result = divide(1, 3)  # 0.3333333333333333
result = divide(22, 7)  # 3.142857142857143
```

#### Exponentiation

```python
# Basic powers
result = power(2, 3)  # 8
result = power(5, 2)  # 25
result = power(10, 0)  # 1

# Negative exponents
result = power(2, -3)  # 0.125
result = power(4, -2)  # 0.0625

# Fractional exponents (roots)
result = power(9, 0.5)  # 3.0 (square root)
result = power(8, 1/3)  # 2.0 (cube root)
```

#### Modulo Operation

```python
# Basic modulo
result = modulo(10, 3)  # 1
result = modulo(15, 4)  # 3
result = modulo(20, 5)  # 0

# Negative numbers
result = modulo(-7, 3)  # 2
result = modulo(7, -3)  # -2
```

### Error Handling for Arithmetic

```python
from mathgenius.core.errors import ValidationError, CalculationError

# Invalid input types
try:
    add("5", 3)  # String input
except ValidationError as e:
    print(f"Validation error: {e}")

# Division by zero
try:
    divide(10, 0)
except CalculationError as e:
    print(f"Calculation error: {e}")

# Modulo by zero
try:
    modulo(10, 0)
except CalculationError as e:
    print(f"Calculation error: {e}")
```

## Algebra Functions

### Linear Equations

Solve linear equations of the form `ax + b = 0`:

```python
# Solve 2x - 6 = 0
# Expected: x = 3
solution = solve_linear(2, -6)  # 3

# Solve 3x + 9 = 0
# Expected: x = -3
solution = solve_linear(3, 9)  # -3

# Solve -x + 5 = 0
# Expected: x = 5
solution = solve_linear(-1, 5)  # 5

# Solve 0x + 0 = 0 (infinite solutions)
solution = solve_linear(0, 0)  # 0 (degenerate case)
```

### Quadratic Equations

Solve quadratic equations of the form `ax² + bx + c = 0`:

```python
# Solve x² - 5x + 6 = 0
# Expected: x = 2 or x = 3
solutions = solve_quadratic(1, -5, 6)  # [2, 3]

# Solve x² - 4 = 0
# Expected: x = ±2
solutions = solve_quadratic(1, 0, -4)  # [-2, 2]

# Solve x² + 2x + 1 = 0
# Expected: x = -1 (double root)
solutions = solve_quadratic(1, 2, 1)  # [-1]

# Solve x² + x + 1 = 0
# Expected: complex solutions
solutions = solve_quadratic(1, 1, 1)  # [-1/2 - sqrt(3)*I/2, -1/2 + sqrt(3)*I/2]
```

### Polynomial Operations

The library uses SymPy for symbolic polynomial manipulation:

#### Expression Expansion

```python
from sympy import symbols

# Define symbols
x, y = symbols('x y')

# Expand (x + 2)(x - 3)
expr = (x + 2) * (x - 3)
expanded = expand_expr(expr)  # x**2 - x - 6

# Expand (x + y)²
expr = (x + y)**2
expanded = expand_expr(expr)  # x**2 + 2*x*y + y**2

# Expand (x + 1)(x² - x + 1)
expr = (x + 1) * (x**2 - x + 1)
expanded = expand_expr(expr)  # x**3 + 1
```

#### Expression Factoring

```python
from sympy import symbols

x = symbols('x')

# Factor x² - 4
expr = x**2 - 4
factored = factor_expr(expr)  # (x - 2)*(x + 2)

# Factor x² + 2x + 1
expr = x**2 + 2*x + 1
factored = factor_expr(expr)  # (x + 1)**2

# Factor x³ - 8
expr = x**3 - 8
factored = factor_expr(expr)  # (x - 2)*(x**2 + 2*x + 4)
```

#### Expression Simplification

```python
from sympy import symbols, sin, cos

x = symbols('x')

# Simplify rational expressions
expr = (x**2 - 1) / (x - 1)
simplified = simplify_expr(expr)  # x + 1

# Simplify trigonometric expressions
expr = sin(x)**2 + cos(x)**2
simplified = simplify_expr(expr)  # 1

# Simplify complex fractions
expr = (x + 1) / (x**2 + 2*x + 1)
simplified = simplify_expr(expr)  # 1/(x + 1)
```

## Complex Examples

### Solving Real-World Problems

#### Problem 1: Projectile Motion

```python
from sympy import symbols

# A projectile's height h(t) = -16t² + 64t + 80
# Find when it hits the ground (h = 0)
t = symbols('t')

# Solve -16t² + 64t + 80 = 0
solutions = solve_quadratic(-16, 64, 80)
print(f"Projectile hits ground at t = {solutions} seconds")

# Find the maximum height time (vertex of parabola)
# t = -b/(2a) = -64/(2*-16) = 2 seconds
max_time = divide(-64, multiply(2, -16))  # 2.0
print(f"Maximum height at t = {max_time} seconds")
```

#### Problem 2: Business Revenue

```python
# Revenue R = price × quantity = p × (1000 - 10p)
# Find price that maximizes revenue
p = symbols('p')

# Expand revenue function
revenue = p * (1000 - 10*p)
expanded_revenue = expand_expr(revenue)  # -10*p**2 + 1000*p

# Find maximum by setting derivative to 0
# dR/dp = -20p + 1000 = 0
# Solve for p
optimal_price = solve_linear(-20, 1000)  # 50
print(f"Optimal price: ${optimal_price}")

# Calculate maximum revenue
max_revenue = multiply(optimal_price, subtract(1000, multiply(10, optimal_price)))
print(f"Maximum revenue: ${max_revenue}")
```

#### Problem 3: Compound Interest

```python
# Compound interest: A = P(1 + r)^t
# Find time needed to double money at 5% annual interest

# Starting amount: $1000, Target: $2000, Rate: 5%
P = 1000
A = 2000
r = 0.05

# Need to solve: 2000 = 1000(1.05)^t
# Simplify: 2 = (1.05)^t
# This requires logarithms (covered in advanced math)

# For now, let's solve a simpler linear approximation
# Using simple interest: A = P(1 + rt)
# 2000 = 1000(1 + 0.05t)
# 2 = 1 + 0.05t
# 1 = 0.05t
time_simple = divide(1, 0.05)  # 20 years
print(f"Time to double with simple interest: {time_simple} years")
```

### Working with Polynomial Sequences

```python
from sympy import symbols

n = symbols('n')

# Arithmetic sequence: a_n = 2n + 3
# Find the 10th term
a_n = 2*n + 3
term_10 = a_n.subs(n, 10)  # 23

# Geometric sequence sum formula
# S_n = a(1 - r^n)/(1 - r)
# For a = 2, r = 3, find S_5
a, r = 2, 3
S_5 = multiply(a, divide(subtract(1, power(r, 5)), subtract(1, r)))
print(f"Sum of first 5 terms: {S_5}")  # 242
```

## Error Handling

### Input Validation

```python
from mathgenius.core.errors import ValidationError, CalculationError

# Invalid input types
try:
    add("hello", 5)
except ValidationError as e:
    print(f"Input validation failed: {e}")

try:
    solve_linear("a", 5)
except ValidationError as e:
    print(f"Equation solving failed: {e}")

# Mathematical errors
try:
    divide(5, 0)
except CalculationError as e:
    print(f"Mathematical error: {e}")

try:
    modulo(10, 0)
except CalculationError as e:
    print(f"Mathematical error: {e}")
```

### Symbolic Expression Errors

```python
# Invalid symbolic expressions
try:
    factor_expr(None)
except ValidationError as e:
    print(f"Expression error: {e}")

try:
    expand_expr("invalid_expression")
except ValidationError as e:
    print(f"Expression error: {e}")
```

## Performance Considerations

### Arithmetic Operations

```python
import time

# Basic operations are very fast
start = time.time()
for i in range(10000):
    result = add(i, i+1)
end = time.time()
print(f"10,000 additions took {end - start:.6f} seconds")

# Division is slightly slower due to zero-check
start = time.time()
for i in range(1, 10001):
    result = divide(i, 2)
end = time.time()
print(f"10,000 divisions took {end - start:.6f} seconds")
```

### Symbolic Operations

```python
from sympy import symbols

# Symbolic operations are more computationally intensive
x = symbols('x')

# Simple polynomial operations
start = time.time()
for i in range(100):
    expr = (x + i)**2
    expanded = expand_expr(expr)
end = time.time()
print(f"100 expansions took {end - start:.6f} seconds")
```

## API Reference

### Arithmetic Functions

All arithmetic functions follow the same pattern:

```python
def operation(a, b):
    """
    Perform mathematical operation on two numbers.
    
    Args:
        a (int|float): First operand
        b (int|float): Second operand
    
    Returns:
        int|float: Result of the operation
    
    Raises:
        ValidationError: If inputs are not valid numbers
        CalculationError: If operation is mathematically invalid
    """
```

### Algebra Functions

```python
def solve_linear(a, b):
    """
    Solve linear equation ax + b = 0.
    
    Args:
        a (int|float): Coefficient of x
        b (int|float): Constant term
    
    Returns:
        float: Solution for x
    
    Raises:
        ValidationError: If inputs are not valid numbers
    """

def solve_quadratic(a, b, c):
    """
    Solve quadratic equation ax² + bx + c = 0.
    
    Args:
        a (int|float): Coefficient of x²
        b (int|float): Coefficient of x
        c (int|float): Constant term
    
    Returns:
        list: List of solutions (may include complex numbers)
    
    Raises:
        ValidationError: If inputs are not valid numbers
    """
```

### Import Options

```python
# Import all functions from unified API
from mathgenius.api.dispatcher import *

# Import specific modules
from mathgenius.arithmetic import operations
from mathgenius.algebra import equations, polynomials

# Import specific functions
from mathgenius.arithmetic.operations import add, subtract, multiply
from mathgenius.algebra.equations import solve_linear, solve_quadratic
```

## Testing

The library includes comprehensive tests for all functionality:

```python
# Run all tests
pytest tests/

# Run specific test modules
pytest tests/test_arithmetic.py
pytest tests/test_algebra.py

# Run with coverage
pytest --cov=mathgenius tests/
```

## Next Steps

Story 1 provides the foundation for more advanced mathematical operations. The next phase (Story 2) adds:

- Geometric calculations
- Trigonometric functions
- Coordinate geometry
- Spatial operations

For advanced mathematical operations (Story 3), see:
- Calculus operations
- Linear algebra
- Statistics and probability
- Symbolic mathematics
