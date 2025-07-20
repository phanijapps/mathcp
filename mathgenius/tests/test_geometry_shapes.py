"""Tests for geometry shapes module."""

import pytest
import math
from mathgenius.geometry.shapes import (
    triangle_area, triangle_perimeter, triangle_area_heron,
    circle_area, circle_circumference,
    rectangle_area, rectangle_perimeter,
    polygon_area, polygon_perimeter,
    sphere_volume, sphere_surface_area,
    cylinder_volume, cylinder_surface_area,
    cube_volume, cube_surface_area,
    pyramid_volume, pyramid_surface_area
)
from mathgenius.core.errors import ValidationError, CalculationError

class TestTriangleFunctions:
    def test_triangle_area_valid(self):
        assert triangle_area(3, 4) == 6.0
        assert triangle_area(5, 10) == 25.0
    
    def test_triangle_area_invalid_input(self):
        with pytest.raises(ValidationError):
            triangle_area("3", 4)
        with pytest.raises(ValidationError):
            triangle_area(-3, 4)
        with pytest.raises(ValidationError):
            triangle_area(3, 0)
    
    def test_triangle_area_heron_valid(self):
        # 3-4-5 triangle
        result = triangle_area_heron(3, 4, 5)
        assert abs(result - 6.0) < 1e-10
        
        # Equilateral triangle with side 2
        result = triangle_area_heron(2, 2, 2)
        expected = math.sqrt(3)
        assert abs(result - expected) < 1e-10
    
    def test_triangle_area_heron_invalid_triangle(self):
        with pytest.raises(CalculationError):
            triangle_area_heron(1, 2, 5)  # Triangle inequality violation
    
    def test_triangle_perimeter_valid(self):
        assert triangle_perimeter(3, 4, 5) == 12
        assert triangle_perimeter(1, 1, 1) == 3
    
    def test_triangle_perimeter_invalid_triangle(self):
        with pytest.raises(CalculationError):
            triangle_perimeter(1, 2, 5)

class TestCircleFunctions:
    def test_circle_area_valid(self):
        result = circle_area(1)
        assert abs(result - math.pi) < 1e-10
        
        result = circle_area(2)
        assert abs(result - 4 * math.pi) < 1e-10
    
    def test_circle_area_invalid(self):
        with pytest.raises(ValidationError):
            circle_area(0)
        with pytest.raises(ValidationError):
            circle_area(-1)
    
    def test_circle_circumference_valid(self):
        result = circle_circumference(1)
        assert abs(result - 2 * math.pi) < 1e-10
        
        result = circle_circumference(3)
        assert abs(result - 6 * math.pi) < 1e-10

class TestRectangleFunctions:
    def test_rectangle_area_valid(self):
        assert rectangle_area(3, 4) == 12
        assert rectangle_area(5, 5) == 25
    
    def test_rectangle_area_invalid(self):
        with pytest.raises(ValidationError):
            rectangle_area(0, 4)
        with pytest.raises(ValidationError):
            rectangle_area(-3, 4)
    
    def test_rectangle_perimeter_valid(self):
        assert rectangle_perimeter(3, 4) == 14
        assert rectangle_perimeter(5, 5) == 20

class TestPolygonFunctions:
    def test_polygon_area_square(self):
        # Square with side 2
        square = [(0, 0), (2, 0), (2, 2), (0, 2)]
        assert polygon_area(square) == 4.0
    
    def test_polygon_area_triangle(self):
        # Right triangle
        triangle = [(0, 0), (3, 0), (0, 4)]
        assert polygon_area(triangle) == 6.0
    
    def test_polygon_perimeter_square(self):
        square = [(0, 0), (2, 0), (2, 2), (0, 2)]
        assert polygon_perimeter(square) == 8.0
    
    def test_polygon_invalid_input(self):
        with pytest.raises(ValidationError):
            polygon_area([(0, 0), (1, 1)])  # Too few points
        with pytest.raises(ValidationError):
            polygon_area([(0, 0), (1, 1, 2)])  # 3D point in 2D function

class TestSphere3DFunctions:
    def test_sphere_volume_valid(self):
        result = sphere_volume(1)
        expected = (4/3) * math.pi
        assert abs(result - expected) < 1e-10
    
    def test_sphere_surface_area_valid(self):
        result = sphere_surface_area(1)
        expected = 4 * math.pi
        assert abs(result - expected) < 1e-10
    
    def test_sphere_invalid_input(self):
        with pytest.raises(ValidationError):
            sphere_volume(0)
        with pytest.raises(ValidationError):
            sphere_surface_area(-1)

class TestCylinderFunctions:
    def test_cylinder_volume_valid(self):
        result = cylinder_volume(1, 2)
        expected = 2 * math.pi
        assert abs(result - expected) < 1e-10
    
    def test_cylinder_surface_area_valid(self):
        result = cylinder_surface_area(1, 2)
        expected = 2 * math.pi * 1 * (1 + 2)  # 2πr(r+h)
        assert abs(result - expected) < 1e-10

class TestCubeFunctions:
    def test_cube_volume_valid(self):
        assert cube_volume(2) == 8
        assert cube_volume(3) == 27
    
    def test_cube_surface_area_valid(self):
        assert cube_surface_area(2) == 24
        assert cube_surface_area(3) == 54

class TestPyramidFunctions:
    def test_pyramid_volume_valid(self):
        # Base area 12, height 4
        result = pyramid_volume(12, 4)
        expected = (1/3) * 12 * 4
        assert abs(result - expected) < 1e-10
    
    def test_pyramid_surface_area_valid(self):
        # Base area 16, perimeter 16, slant height 5
        result = pyramid_surface_area(16, 16, 5)
        expected = 16 + (0.5 * 16 * 5)
        assert abs(result - expected) < 1e-10
