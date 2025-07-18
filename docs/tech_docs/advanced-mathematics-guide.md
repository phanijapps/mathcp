# Advanced Mathematics Guide - Story 3

## Overview
This guide covers the advanced mathematical functionality implemented in Math Genius Story 3, including calculus, linear algebra, statistics, and symbolic mathematics operations.

## Table of Contents
1. [Calculus Operations](#calculus-operations)
2. [Linear Algebra Operations](#linear-algebra-operations)
3. [Statistics and Probability](#statistics-and-probability)
4. [Symbolic Mathematics](#symbolic-mathematics)
5. [API Reference](#api-reference)
6. [Error Handling](#error-handling)
7. [Performance Considerations](#performance-considerations)
8. [Examples and Use Cases](#examples-and-use-cases)

---

## Calculus Operations

### Symbolic Calculus
The calculus module provides comprehensive symbolic and numerical calculus operations powered by SymPy.

#### Differentiation
```python
from mathgenius.advanced.calculus import differentiate

# Basic differentiation
result = differentiate("x**2", "x")  # Returns: 2*x
result = differentiate("sin(x)", "x")  # Returns: cos(x)

# Higher order derivatives
result = differentiate("x**3", "x", order=2)  # Returns: 6*x
```

#### Integration
```python
from mathgenius.advanced.calculus import integrate_definite, integrate_indefinite

# Indefinite integration
result = integrate_indefinite("x**2", "x")  # Returns: x**3/3

# Definite integration
result = integrate_definite("x**2", "x", 0, 2)  # Returns: 8/3
```

#### Limits
```python
from mathgenius.advanced.calculus import compute_limit

# Basic limits
result = compute_limit("sin(x)/x", "x", 0)  # Returns: 1

# Limits at infinity
result = compute_limit("1/x", "x", "oo")  # Returns: 0
```

#### Series Expansions
```python
from mathgenius.advanced.calculus import taylor_series

# Taylor series expansion
result = taylor_series("exp(x)", "x", 0, 4)
# Returns: 1 + x + x**2/2 + x**3/6 + x**4/24
```

### Multivariable Calculus
```python
from mathgenius.advanced.calculus import partial_derivative, gradient, hessian_matrix

# Partial derivatives
result = partial_derivative("x**2 + y**2", "x")  # Returns: 2*x

# Gradient calculation
result = gradient("x**2 + y**2", ["x", "y"])  # Returns: [2*x, 2*y]

# Hessian matrix
result = hessian_matrix("x**2 + y**2", ["x", "y"])
# Returns: [[2, 0], [0, 2]]
```

### Numerical Methods
```python
from mathgenius.advanced.calculus import numerical_derivative, numerical_integral

# Numerical derivative
def f(x):
    return x**2
result = numerical_derivative(f, 2)  # Returns: 4.0

# Numerical integration
result = numerical_integral(f, 0, 1, method='simpson')  # Returns: 0.333...
```

---

## Linear Algebra Operations

### Matrix Operations
```python
from mathgenius.advanced.linear_algebra import (
    matrix_add, matrix_multiply, matrix_transpose, matrix_inverse
)

# Matrix addition
a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
result = matrix_add(a, b)  # Returns: [[6, 8], [10, 12]]

# Matrix multiplication
result = matrix_multiply(a, b)  # Returns: [[19, 22], [43, 50]]

# Matrix transpose
result = matrix_transpose(a)  # Returns: [[1, 3], [2, 4]]

# Matrix inverse
result = matrix_inverse(a)  # Returns: [[-2, 1], [1.5, -0.5]]
```

### Matrix Properties
```python
from mathgenius.advanced.linear_algebra import (
    matrix_determinant, matrix_trace, matrix_rank
)

# Determinant
result = matrix_determinant([[1, 2], [3, 4]])  # Returns: -2

# Trace
result = matrix_trace([[1, 2], [3, 4]])  # Returns: 5

# Rank
result = matrix_rank([[1, 2], [3, 4]])  # Returns: 2
```

### Eigenvalues and Eigenvectors
```python
from mathgenius.advanced.linear_algebra import eigenvalues_eigenvectors

eigenvals, eigenvecs = eigenvalues_eigenvectors([[1, 2], [2, 1]])
# Returns eigenvalues and corresponding eigenvectors
```

### Linear Systems
```python
from mathgenius.advanced.linear_algebra import solve_linear_system

# Solve Ax = b
a = [[1, 2], [3, 4]]
b = [5, 11]
result = solve_linear_system(a, b)  # Returns: [1, 2]
```

### Matrix Decompositions
```python
from mathgenius.advanced.linear_algebra import (
    lu_decomposition, qr_decomposition, svd_decomposition
)

# LU decomposition
p, l, u = lu_decomposition([[1, 2], [3, 4]])

# QR decomposition
q, r = qr_decomposition([[1, 2], [3, 4]])

# SVD decomposition
u, s, vt = svd_decomposition([[1, 2], [3, 4]])
```

### Vector Operations
```python
from mathgenius.advanced.linear_algebra import vector_norm, vector_projection

# Vector norm
result = vector_norm([3, 4])  # Returns: 5.0

# Vector projection
result = vector_projection([1, 2], [3, 0])  # Returns: [1, 0]
```

---

## Statistics and Probability

### Descriptive Statistics
```python
from mathgenius.advanced.statistics import (
    mean, median, mode, variance, standard_deviation
)

data = [1, 2, 3, 4, 5]

# Central tendency
mean_val = mean(data)  # Returns: 3.0
median_val = median(data)  # Returns: 3.0
mode_val = mode([1, 2, 2, 3, 3, 3])  # Returns: 3.0

# Dispersion
var = variance(data)  # Returns: 2.5 (sample variance)
std = standard_deviation(data)  # Returns: 1.58... (sample std)
```

### Correlation and Covariance
```python
from mathgenius.advanced.statistics import correlation_coefficient, covariance

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Correlation
corr = correlation_coefficient(x, y)  # Returns: 1.0 (perfect correlation)

# Covariance
cov = covariance(x, y)  # Returns: 5.0
```

### Probability Distributions
```python
from mathgenius.advanced.statistics import (
    normal_distribution_pdf, normal_distribution_cdf,
    binomial_distribution_pmf, poisson_distribution_pmf
)

# Normal distribution
pdf = normal_distribution_pdf(0, mean=0, std=1)  # Returns: 0.399...
cdf = normal_distribution_cdf(0, mean=0, std=1)  # Returns: 0.5

# Binomial distribution
pmf = binomial_distribution_pmf(5, 10, 0.5)  # Returns: 0.246...

# Poisson distribution
pmf = poisson_distribution_pmf(2, 2)  # Returns: 0.270...
```

### Hypothesis Testing
```python
from mathgenius.advanced.statistics import (
    t_test_one_sample, t_test_two_sample, chi_square_test
)

# One-sample t-test
result = t_test_one_sample([1, 2, 3, 4, 5], population_mean=0)
# Returns: {'t_statistic': 3.354, 'p_value': 0.028, 'reject_null': True, ...}

# Two-sample t-test
result = t_test_two_sample([1, 2, 3], [4, 5, 6])
# Returns: {'t_statistic': -3.464, 'p_value': 0.021, 'reject_null': True, ...}

# Chi-square test
result = chi_square_test([10, 15, 20], [15, 15, 15])
# Returns: {'chi2_statistic': 1.667, 'p_value': 0.435, 'reject_null': False, ...}
```

### Regression Analysis
```python
from mathgenius.advanced.statistics import linear_regression

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

result = linear_regression(x, y)
# Returns: {'slope': 2.0, 'intercept': 0.0, 'r_squared': 1.0, ...}
```

### Confidence Intervals
```python
from mathgenius.advanced.statistics import confidence_interval

result = confidence_interval([1, 2, 3, 4, 5], confidence_level=0.95)
# Returns: {'mean': 3.0, 'lower_bound': 1.24, 'upper_bound': 4.76, ...}
```

---

## Symbolic Mathematics

### Expression Parsing and Creation
```python
from mathgenius.advanced.symbolic import parse_expression, create_symbol

# Parse expression
expr = parse_expression("x**2 + 2*x + 1")

# Create symbol with assumptions
x = create_symbol("x", {"real": True, "positive": True})
```

### Expression Manipulation
```python
from mathgenius.advanced.symbolic import (
    expand_expression, factor_expression, simplify_expression
)

# Expand expression
result = expand_expression("(x + 1)**2")  # Returns: x**2 + 2*x + 1

# Factor expression
result = factor_expression("x**2 + 2*x + 1")  # Returns: (x + 1)**2

# Simplify expression
result = simplify_expression("sin(x)**2 + cos(x)**2")  # Returns: 1
```

### Equation Solving
```python
from mathgenius.advanced.symbolic import solve_equation, solve_differential_equation

# Solve algebraic equation
result = solve_equation("x**2 - 4", "x")  # Returns: [-2, 2]

# Solve system of equations
result = solve_equation(["x + y - 3", "x - y - 1"], ["x", "y"])
# Returns: [{'x': 2, 'y': 1}]

# Solve differential equation
result = solve_differential_equation("Derivative(y(x), x) - y(x)", "y")
# Returns: y(x) = C1*exp(x)
```

### Expression Evaluation and Substitution
```python
from mathgenius.advanced.symbolic import (
    substitute_expression, evaluate_expression
)

# Substitute values
result = substitute_expression("x**2 + 2*x + 1", {"x": 3})  # Returns: 16

# Evaluate expression
result = evaluate_expression("2 + 3 * 4")  # Returns: 14
```

### Symbolic Calculus
```python
from mathgenius.advanced.symbolic import (
    symbolic_integrate, symbolic_differentiate, symbolic_limit, symbolic_series
)

# Symbolic differentiation
result = symbolic_differentiate("x**3", "x")  # Returns: 3*x**2

# Symbolic integration
result = symbolic_integrate("x**2", "x")  # Returns: x**3/3

# Symbolic limit
result = symbolic_limit("sin(x)/x", "x", 0)  # Returns: 1

# Symbolic series
result = symbolic_series("exp(x)", "x", 0, 4)
# Returns: 1 + x + x**2/2 + x**3/6 + x**4/24
```

### Expression Formatting
```python
from mathgenius.advanced.symbolic import (
    expression_to_latex, expression_to_string
)

# Convert to LaTeX
latex = expression_to_latex("x**2 + 2*x + 1")  # Returns: "x^{2} + 2 x + 1"

# Convert to string
string = expression_to_string("x**2 + 2*x + 1", pretty_print=True)
```

---

## API Reference

All advanced mathematics functions are accessible through the unified API:

```python
from mathgenius.api.dispatcher import *

# All functions from calculus, linear algebra, statistics, and symbolic modules
# are available directly through the dispatcher
```

### Function Categories

#### Calculus Functions
- `differentiate(expression, variable, order=1)`
- `integrate_definite(expression, variable, lower_bound, upper_bound)`
- `integrate_indefinite(expression, variable)`
- `compute_limit(expression, variable, point, direction='+')`
- `taylor_series(expression, variable, point=0, order=6)`
- `partial_derivative(expression, variable, order=1)`
- `gradient(expression, variables)`
- `hessian_matrix(expression, variables)`
- `numerical_derivative(func, point, h=1e-8)`
- `numerical_integral(func, lower_bound, upper_bound, method='simpson', n=1000)`

#### Linear Algebra Functions
- `matrix_add(matrix_a, matrix_b)`
- `matrix_multiply(matrix_a, matrix_b)`
- `matrix_transpose(matrix)`
- `matrix_inverse(matrix)`
- `matrix_determinant(matrix)`
- `eigenvalues_eigenvectors(matrix)`
- `solve_linear_system(matrix_a, vector_b)`
- `matrix_rank(matrix)`
- `matrix_nullspace(matrix)`
- `lu_decomposition(matrix)`
- `qr_decomposition(matrix)`
- `svd_decomposition(matrix)`
- `vector_norm(vector, ord=2)`
- `matrix_condition_number(matrix)`
- `matrix_trace(matrix)`
- `vector_projection(vector_a, vector_b)`

#### Statistics Functions
- `mean(data)`
- `median(data)`
- `mode(data)`
- `variance(data, ddof=1)`
- `standard_deviation(data, ddof=1)`
- `correlation_coefficient(data_x, data_y)`
- `covariance(data_x, data_y, ddof=1)`
- `normal_distribution_pdf(x, mean=0, std=1)`
- `normal_distribution_cdf(x, mean=0, std=1)`
- `binomial_distribution_pmf(k, n, p)`
- `poisson_distribution_pmf(k, mu)`
- `t_test_one_sample(data, population_mean, alpha=0.05)`
- `t_test_two_sample(data1, data2, alpha=0.05, equal_var=True)`
- `chi_square_test(observed, expected=None, alpha=0.05)`
- `linear_regression(x_data, y_data)`
- `confidence_interval(data, confidence_level=0.95)`
- `z_score(value, mean, std)`
- `percentile(data, percentile_value)`

#### Symbolic Mathematics Functions
- `parse_expression(expression_string)`
- `create_symbol(symbol_name, assumptions=None)`
- `expand_expression(expression)`
- `factor_expression(expression)`
- `simplify_expression(expression)`
- `collect_terms(expression, variable)`
- `solve_equation(equation, variable=None)`
- `solve_differential_equation(equation, function=None)`
- `substitute_expression(expression, substitutions)`
- `evaluate_expression(expression, substitutions=None)`
- `expression_to_latex(expression)`
- `expression_to_string(expression, pretty_print=False)`
- `symbolic_integrate(expression, variable, limits=None)`
- `symbolic_differentiate(expression, variable, order=1)`
- `symbolic_limit(expression, variable, point, direction='+')`
- `symbolic_series(expression, variable, point=0, order=6)`
- `create_rational(numerator, denominator)`
- `is_polynomial(expression, variable=None)`

---

## Error Handling

All advanced mathematics functions implement comprehensive error handling:

### ValidationError
Raised when input parameters are invalid:
```python
from mathgenius.core.errors import ValidationError

try:
    result = differentiate("x**2", "x", order=0)  # Invalid order
except ValidationError as e:
    print(f"Input validation error: {e}")
```

### CalculationError
Raised when mathematical computation fails:
```python
from mathgenius.core.errors import CalculationError

try:
    result = matrix_inverse([[1, 2], [2, 4]])  # Singular matrix
except CalculationError as e:
    print(f"Calculation error: {e}")
```

### Common Error Scenarios
1. **Invalid expressions**: Malformed mathematical expressions
2. **Dimension mismatches**: Incompatible matrix/vector dimensions
3. **Singular matrices**: Attempting to invert non-invertible matrices
4. **Convergence issues**: Numerical methods failing to converge
5. **Domain violations**: Operations outside valid mathematical domains

---

## Performance Considerations

### Computational Complexity
- **Matrix operations**: O(n³) for most operations on n×n matrices
- **Eigenvalue computation**: O(n³) for n×n matrices
- **Symbolic operations**: Varies greatly based on expression complexity
- **Numerical integration**: O(n) where n is the number of intervals

### Memory Usage
- **Large matrices**: Consider using sparse matrices for large, sparse systems
- **Symbolic expressions**: Complex expressions can consume significant memory
- **Numerical methods**: Higher precision requires more memory

### Optimization Tips
1. **Use appropriate precision**: Don't use higher precision than necessary
2. **Vectorize operations**: Use NumPy arrays for better performance
3. **Choose efficient algorithms**: Select appropriate methods for your problem size
4. **Memory management**: Be mindful of memory usage with large datasets

---

## Examples and Use Cases

### Scientific Computing
```python
# Solve a system of differential equations
from mathgenius.advanced.symbolic import solve_differential_equation
from mathgenius.advanced.calculus import numerical_integral

# Population dynamics model
equation = "Derivative(P(t), t) - r*P(t)*(1 - P(t)/K)"
solution = solve_differential_equation(equation, "P")
```

### Engineering Applications
```python
# Structural analysis with linear algebra
from mathgenius.advanced.linear_algebra import solve_linear_system, matrix_determinant

# Solve structural equilibrium equations
stiffness_matrix = [[100, -50, 0], [-50, 150, -100], [0, -100, 100]]
force_vector = [1000, 500, 0]
displacements = solve_linear_system(stiffness_matrix, force_vector)
```

### Data Analysis
```python
# Statistical analysis of experimental data
from mathgenius.advanced.statistics import (
    mean, standard_deviation, t_test_one_sample, confidence_interval
)

experimental_data = [23.1, 24.5, 22.8, 25.2, 23.9, 24.1, 22.5, 24.8]
sample_mean = mean(experimental_data)
sample_std = standard_deviation(experimental_data)

# Test if mean is significantly different from theoretical value
test_result = t_test_one_sample(experimental_data, theoretical_mean=24.0)
conf_int = confidence_interval(experimental_data, confidence_level=0.95)
```

### Mathematical Modeling
```python
# Symbolic analysis of mathematical models
from mathgenius.advanced.symbolic import (
    parse_expression, symbolic_differentiate, solve_equation
)

# Analyze critical points of a function
function = "x**3 - 3*x**2 + 2*x"
derivative = symbolic_differentiate(function, "x")
critical_points = solve_equation(derivative, "x")
```

---

## Dependencies

The advanced mathematics functionality requires the following libraries:
- **NumPy**: Efficient numerical computations
- **SciPy**: Scientific computing functions
- **SymPy**: Symbolic mathematics
- **scikit-learn**: Machine learning and regression
- **matplotlib**: Plotting and visualization
- **pandas**: Data manipulation and analysis

All dependencies are automatically installed when you install the mathgenius package.

---

## Conclusion

The Math Genius Story 3 advanced mathematics module provides a comprehensive suite of tools for:
- Calculus operations (differentiation, integration, limits, series)
- Linear algebra (matrix operations, eigenvalues, decompositions)
- Statistics and probability (descriptive stats, hypothesis testing, regression)
- Symbolic mathematics (expression manipulation, equation solving)

All functions follow consistent API patterns, provide robust error handling, and are thoroughly tested for reliability and accuracy. The unified API makes it easy to access all functionality through a single import, while the modular design allows for efficient use of specific mathematical domains.

For more information, examples, and updates, visit the [Math Genius documentation](https://github.com/mathgenius/docs).
