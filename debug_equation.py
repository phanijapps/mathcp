#!/usr/bin/env python3
"""Debug equation parsing"""

import sys
import os

# Add the mathgenius package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mathgenius'))

from sympy import symbols, sympify

def debug_parsing():
    print("Debugging equation parsing...")
    
    # Test the parsing step by step
    equation = "x^3 - 6*x^2 + 11*x - 6 = 0"
    print(f"Original equation: {equation}")
    
    # Split on =
    left_side, right_side = equation.split('=', 1)
    print(f"Left side: '{left_side.strip()}'")
    print(f"Right side: '{right_side.strip()}'")
    
    # Replace ^ with **
    left_side = left_side.replace('^', '**')
    right_side = right_side.replace('^', '**')
    print(f"After ^ replacement - Left: '{left_side.strip()}'")
    print(f"After ^ replacement - Right: '{right_side.strip()}'")
    
    # Try to parse
    try:
        x = symbols('x')
        left_expr = sympify(left_side.strip())
        print(f"Left expression parsed successfully: {left_expr}")
        
        right_expr = sympify(right_side.strip())
        print(f"Right expression parsed successfully: {right_expr}")
        
    except Exception as e:
        print(f"Parsing failed: {e}")
        
        # Try a different approach - maybe the issue is with the multiplication
        print("\nTrying alternative parsing...")
        
        # Replace implicit multiplication
        left_modified = left_side.strip()
        # Add explicit multiplication for patterns like "6*x"
        import re
        left_modified = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', left_modified)
        print(f"Modified left side: '{left_modified}'")
        
        try:
            left_expr = sympify(left_modified)
            print(f"Modified left expression parsed: {left_expr}")
        except Exception as e2:
            print(f"Modified parsing also failed: {e2}")

if __name__ == "__main__":
    debug_parsing()
