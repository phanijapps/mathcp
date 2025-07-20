# Math Genius API Reference

## Arithmetic Functions
- `add(a, b)`
- `subtract(a, b)`
- `multiply(a, b)`
- `divide(a, b)`
- `power(a, b)`
- `modulo(a, b)`

**Example:**
```python
from mathgenius.api import add
add(2, 3)  # 5
```

## Algebraic Functions
- `solve_linear(a, b)`
- `solve_quadratic(a, b, c)`
- `expand_expr(expr)`
- `factor_expr(expr)`
- `simplify_expr(expr)`

**Example:**
```python
from mathgenius.api import solve_quadratic
solve_quadratic(1, -3, 2)  # [1, 2]
```

## Error Handling
All functions raise `ValidationError` or `CalculationError` for invalid input or math errors.

**Example:**
```python
from mathgenius.api import divide
from mathgenius.core.errors import CalculationError
try:
    divide(1, 0)
except CalculationError as e:
    print(e)
```
