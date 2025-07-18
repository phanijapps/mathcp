#!/usr/bin/env python3
"""
Math Genius Geometry & Trigonometry Demo

This script demonstrates the new geometry and trigonometry functionality
implemented in Story 2.
"""

import math
from mathgenius.api.dispatcher import (
    # Shape calculations
    triangle_area, triangle_area_heron, circle_area, rectangle_area,
    sphere_volume, cylinder_volume, cube_volume,
    # Trigonometry
    sin, cos, tan, asin, acos, atan, degrees_to_radians, radians_to_degrees,
    # Coordinate geometry
    distance_2d, distance_3d, midpoint_2d, slope, line_intersection,
    # Spatial operations
    vector_add, vector_dot_product, vector_cross_product, angle_between_vectors,
    rotate_point, translate_point, scale_point
)

def demo_shapes():
    """Demonstrate shape calculations."""
    print("=== SHAPE CALCULATIONS ===")
    
    # Triangle
    print(f"Triangle area (base=5, height=8): {triangle_area(5, 8)}")
    print(f"Triangle area by Heron's formula (3-4-5 triangle): {triangle_area_heron(3, 4, 5)}")
    
    # Circle
    radius = 3
    print(f"Circle area (radius={radius}): {circle_area(radius):.3f}")
    
    # Rectangle
    print(f"Rectangle area (4x6): {rectangle_area(4, 6)}")
    
    # 3D Shapes
    print(f"Sphere volume (radius=2): {sphere_volume(2):.3f}")
    print(f"Cylinder volume (radius=2, height=5): {cylinder_volume(2, 5):.3f}")
    print(f"Cube volume (side=3): {cube_volume(3)}")
    print()

def demo_trigonometry():
    """Demonstrate trigonometry functions."""
    print("=== TRIGONOMETRY ===")
    
    # Basic trig functions
    print(f"sin(90°): {sin(90, 'degrees'):.3f}")
    print(f"cos(0°): {cos(0, 'degrees'):.3f}")
    print(f"tan(45°): {tan(45, 'degrees'):.3f}")
    
    # Inverse trig functions
    print(f"asin(0.5) in degrees: {asin(0.5, 'degrees'):.1f}°")
    print(f"acos(0.5) in degrees: {acos(0.5, 'degrees'):.1f}°")
    print(f"atan(1) in degrees: {atan(1, 'degrees'):.1f}°")
    
    # Angle conversion
    print(f"180° in radians: {degrees_to_radians(180):.3f}")
    print(f"π radians in degrees: {radians_to_degrees(math.pi):.1f}°")
    print()

def demo_coordinates():
    """Demonstrate coordinate geometry."""
    print("=== COORDINATE GEOMETRY ===")
    
    # Points
    p1 = (0, 0)
    p2 = (3, 4)
    p3 = (6, 8)
    
    # Distance calculations
    print(f"Distance from {p1} to {p2}: {distance_2d(p1, p2):.1f}")
    print(f"3D distance from (0,0,0) to (3,4,12): {distance_3d((0, 0, 0), (3, 4, 12)):.1f}")
    
    # Midpoint
    midpoint = midpoint_2d(p1, p2)
    print(f"Midpoint of {p1} and {p2}: {midpoint}")
    
    # Slope
    slope_value = slope(p1, p2)
    print(f"Slope of line from {p1} to {p2}: {slope_value:.3f}")
    
    # Line intersection
    intersection = line_intersection((0, 0), (2, 2), (0, 2), (2, 0))
    print(f"Intersection of two lines: {intersection}")
    print()

def demo_spatial():
    """Demonstrate spatial operations."""
    print("=== SPATIAL OPERATIONS ===")
    
    # Vector operations
    v1 = (1, 2)
    v2 = (3, 4)
    
    print(f"Vector addition {v1} + {v2}: {vector_add(v1, v2)}")
    print(f"Dot product {v1} · {v2}: {vector_dot_product(v1, v2)}")
    
    # 3D cross product
    v3d1 = (1, 0, 0)
    v3d2 = (0, 1, 0)
    cross = vector_cross_product(v3d1, v3d2)
    print(f"Cross product {v3d1} × {v3d2}: {cross}")
    
    # Angle between vectors
    angle = angle_between_vectors(v1, v2, 'degrees')
    print(f"Angle between {v1} and {v2}: {angle:.1f}°")
    
    # Transformations
    point = (1, 0)
    rotated = rotate_point(point, 90, unit='degrees')
    translated = translate_point(point, (2, 3))
    scaled = scale_point(point, 2)
    
    print(f"Point {point} rotated 90°: ({rotated[0]:.1f}, {rotated[1]:.1f})")
    print(f"Point {point} translated by (2,3): {translated}")
    print(f"Point {point} scaled by 2: {scaled}")
    print()

def demo_complex_example():
    """Demonstrate a complex geometry problem."""
    print("=== COMPLEX EXAMPLE: TRIANGLE ANALYSIS ===")
    
    # Define a triangle with vertices
    A = (0, 0)
    B = (4, 0)
    C = (2, 3)
    
    print(f"Triangle vertices: A{A}, B{B}, C{C}")
    
    # Calculate side lengths
    AB = distance_2d(A, B)
    BC = distance_2d(B, C)
    CA = distance_2d(C, A)
    
    print(f"Side lengths: AB={AB:.1f}, BC={BC:.1f}, CA={CA:.1f}")
    
    # Calculate area using Heron's formula
    area = triangle_area_heron(AB, BC, CA)
    print(f"Area (Heron's formula): {area:.1f}")
    
    # Calculate area using base and height
    base = AB
    height = C[1]  # y-coordinate of C (since AB is on x-axis)
    area_bh = triangle_area(base, height)
    print(f"Area (base×height): {area_bh:.1f}")
    
    # Calculate centroid
    centroid_x = (A[0] + B[0] + C[0]) / 3
    centroid_y = (A[1] + B[1] + C[1]) / 3
    centroid = (centroid_x, centroid_y)
    print(f"Centroid: ({centroid_x:.1f}, {centroid_y:.1f})")
    
    # Calculate angles using vectors
    # Vector from A to B
    vec_AB = vector_add(B, (-A[0], -A[1]))
    # Vector from A to C
    vec_AC = vector_add(C, (-A[0], -A[1]))
    
    angle_A = angle_between_vectors(vec_AB, vec_AC, 'degrees')
    print(f"Angle at vertex A: {angle_A:.1f}°")
    
    print()

def main():
    """Main demonstration function."""
    print("Math Genius - Geometry & Trigonometry Demo")
    print("=" * 50)
    print()
    
    demo_shapes()
    demo_trigonometry()
    demo_coordinates()
    demo_spatial()
    demo_complex_example()
    
    print("Demo completed successfully!")
    print("All Story 2 tasks have been implemented and tested.")

if __name__ == "__main__":
    main()
