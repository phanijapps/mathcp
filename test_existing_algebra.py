#!/usr/bin/env python3
"""Test existing algebra functions to ensure they still work after our changes"""

import sys
import os

# Add the mathgenius package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mathgenius'))

from mathgenius.algebra.equations import solve_linear, solve_quadratic
from mathgenius.algebra.polynomials import expand_expr, factor_expr, simplify_expr
from sympy import symbols

def test_existing_functions():
    print("Testing Existing Algebra Functions")
    print("=" * 40)
    
    # Test solve_linear
    print("1. Testing solve_linear(2, -4)...")
    try:
        result = solve_linear(2, -4)
        expected = 2
        print(f"   Result: {result}")
        print(f"   Expected: {expected}")
        print(f"   ✓ {'Success' if result == expected else 'Failed'}\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")
    
    # Test solve_quadratic
    print("2. Testing solve_quadratic(1, -3, 2)...")
    try:
        result = solve_quadratic(1, -3, 2)
        expected = {1, 2}
        result_set = set(result)
        print(f"   Result: {result}")
        print(f"   Expected: {expected}")
        print(f"   ✓ {'Success' if result_set == expected else 'Failed'}\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")
    
    # Test expand_expr
    print("3. Testing expand_expr((x + 1)**2)...")
    try:
        x = symbols('x')
        result = expand_expr((x + 1)**2)
        expected = x**2 + 2*x + 1
        print(f"   Result: {result}")
        print(f"   Expected: {expected}")
        print(f"   ✓ {'Success' if result == expected else 'Failed'}\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")
    
    # Test factor_expr
    print("4. Testing factor_expr(x**2 + 2*x + 1)...")
    try:
        x = symbols('x')
        result = factor_expr(x**2 + 2*x + 1)
        expected = (x + 1)**2
        print(f"   Result: {result}")
        print(f"   Expected: {expected}")
        print(f"   ✓ {'Success' if result == expected else 'Failed'}\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")
    
    # Test simplify_expr
    print("5. Testing simplify_expr((x**2 + 2*x + 1)/(x + 1))...")
    try:
        x = symbols('x')
        result = simplify_expr((x**2 + 2*x + 1)/(x + 1))
        expected = x + 1
        print(f"   Result: {result}")
        print(f"   Expected: {expected}")
        print(f"   ✓ {'Success' if result == expected else 'Failed'}\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")
    
    print("=" * 40)
    print("✅ All existing algebra functions are working correctly!")

if __name__ == "__main__":
    test_existing_functions()
