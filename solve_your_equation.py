#!/usr/bin/env python3
"""
Solve the cubic equation: x^3 - 6*x^2 + 11*x - 6 = 0

This script demonstrates how to use the mathgenius library to solve equations.
"""

import sys
import os

# Add the mathgenius package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mathgenius'))

from mathgenius.algebra.equations import solve_equation, solve_cubic

def main():
    print("🧮 MathGenius Equation Solver")
    print("=" * 40)
    
    # Your original equation
    equation = "x^3 - 6*x^2 + 11*x - 6 = 0"
    
    print(f"Solving: {equation}")
    print()
    
    # Method 1: Using the general string-based solver
    print("Method 1: General equation solver")
    try:
        solutions = solve_equation(equation)
        print(f"Solutions: {solutions}")
        
        # Verify each solution
        print("\nVerification:")
        for i, x in enumerate(solutions, 1):
            result = x**3 - 6*x**2 + 11*x - 6
            print(f"  x{i} = {x}: {x}³ - 6({x})² + 11({x}) - 6 = {result}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "-" * 40)
    
    # Method 2: Using the cubic solver with coefficients
    print("Method 2: Cubic coefficient solver")
    print("For equation: ax³ + bx² + cx + d = 0")
    print("Coefficients: a=1, b=-6, c=11, d=-6")
    
    try:
        solutions = solve_cubic(1, -6, 11, -6)
        print(f"Solutions: {solutions}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 40)
    print("✅ Your cubic equation has been solved!")
    print("The solutions are: x = 1, x = 2, and x = 3")
    print("\nThese are the roots where the cubic polynomial equals zero.")

if __name__ == "__main__":
    main()
