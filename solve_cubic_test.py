#!/usr/bin/env python3
"""Test script to solve the cubic equation x^3 - 6*x^2 + 11*x - 6 = 0"""

import sys
import os

# Add the mathgenius package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mathgenius'))

from mathgenius.algebra.equations import solve_equation, solve_cubic

def main():
    print("Solving cubic equation: x^3 - 6*x^2 + 11*x - 6 = 0")
    print("=" * 50)
    
    # Method 1: Using the general equation solver
    try:
        equation = "x^3 - 6*x^2 + 11*x - 6 = 0"
        solutions1 = solve_equation(equation, 'x')
        print(f"Method 1 - General solver:")
        print(f"Solutions: {solutions1}")
        print()
    except Exception as e:
        print(f"Method 1 failed: {e}")
        print()
    
    # Method 2: Using the cubic solver with coefficients
    try:
        # For x^3 - 6*x^2 + 11*x - 6 = 0
        # Coefficients are: a=1, b=-6, c=11, d=-6
        solutions2 = solve_cubic(1, -6, 11, -6)
        print(f"Method 2 - Cubic solver:")
        print(f"Solutions: {solutions2}")
        print()
    except Exception as e:
        print(f"Method 2 failed: {e}")
        print()
    
    # Verify solutions by substitution
    if 'solutions1' in locals() and solutions1:
        print("Verification by substitution:")
        print("-" * 30)
        for i, x in enumerate(solutions1):
            try:
                # Calculate x^3 - 6*x^2 + 11*x - 6
                result = x**3 - 6*x**2 + 11*x - 6
                print(f"x = {x}: {x}^3 - 6*{x}^2 + 11*{x} - 6 = {result}")
            except Exception as e:
                print(f"x = {x}: Verification failed - {e}")

if __name__ == "__main__":
    main()
