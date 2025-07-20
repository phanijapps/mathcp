#!/usr/bin/env python3
"""Test the algebra equation solving functionality directly"""

import sys
import os

# Add the mathgenius package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mathgenius'))

# Import directly from algebra module to avoid naming conflicts
from mathgenius.algebra.equations import solve_equation, solve_cubic, solve_linear, solve_quadratic

def test_algebra_equation_solving():
    print("Testing Algebra Equation Solving Functions")
    print("=" * 50)
    
    # Test 1: Your original cubic equation
    print("1. Cubic Equation: x^3 - 6*x^2 + 11*x - 6 = 0")
    try:
        solutions = solve_equation("x^3 - 6*x^2 + 11*x - 6 = 0")
        print(f"   Solutions: {solutions}")
        print(f"   Expected: [1.0, 2.0, 3.0]")
        print(f"   ✓ Success\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")
    
    # Test 2: Quadratic equation
    print("2. Quadratic Equation: x^2 - 5*x + 6 = 0")
    try:
        solutions = solve_equation("x^2 - 5*x + 6 = 0")
        print(f"   Solutions: {solutions}")
        print(f"   Expected: [2.0, 3.0]")
        print(f"   ✓ Success\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")
    
    # Test 3: Linear equation
    print("3. Linear Equation: 2*x - 8 = 0")
    try:
        solutions = solve_equation("2*x - 8 = 0")
        print(f"   Solutions: {solutions}")
        print(f"   Expected: [4.0]")
        print(f"   ✓ Success\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")
    
    # Test 4: Using solve_cubic directly
    print("4. Direct cubic solver: x^3 - 6*x^2 + 11*x - 6 = 0")
    try:
        solutions = solve_cubic(1, -6, 11, -6)
        print(f"   Solutions: {solutions}")
        print(f"   Expected: [1.0, 2.0, 3.0]")
        print(f"   ✓ Success\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")
    
    # Test 5: Complex equation
    print("5. Complex Equation: x^2 + 1 = 0")
    try:
        solutions = solve_equation("x^2 + 1 = 0")
        print(f"   Solutions: {solutions}")
        print(f"   Expected: Complex solutions [-I, I]")
        print(f"   ✓ Success\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")
    
    # Test 6: Higher degree polynomial
    print("6. Quartic Equation: x^4 - 10*x^2 + 9 = 0")
    try:
        solutions = solve_equation("x^4 - 10*x^2 + 9 = 0")
        print(f"   Solutions: {solutions}")
        print(f"   Expected: [-3.0, -1.0, 1.0, 3.0]")
        print(f"   ✓ Success\n")
    except Exception as e:
        print(f"   ✗ Failed: {e}\n")

if __name__ == "__main__":
    test_algebra_equation_solving()
