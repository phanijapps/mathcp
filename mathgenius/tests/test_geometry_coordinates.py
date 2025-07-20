"""Tests for geometry coordinates module."""

import pytest
import math
from mathgenius.geometry.coordinates import (
    distance_2d, distance_3d, midpoint_2d, midpoint_3d,
    slope, line_equation, line_intersection, point_to_line_distance
)
from mathgenius.core.errors import ValidationError, CalculationError

class TestDistanceFunctions:
    def test_distance_2d_valid(self):
        # Basic distance calculation
        result = distance_2d((0, 0), (3, 4))
        assert abs(result - 5) < 1e-10
        
        # Same point
        result = distance_2d((1, 1), (1, 1))
        assert result == 0
        
        # Negative coordinates
        result = distance_2d((-1, -1), (2, 3))
        expected = math.sqrt(9 + 16)  # sqrt(3^2 + 4^2)
        assert abs(result - expected) < 1e-10
    
    def test_distance_2d_invalid(self):
        with pytest.raises(ValidationError):
            distance_2d((0, 0), (1, 2, 3))  # 3D point
        with pytest.raises(ValidationError):
            distance_2d("invalid", (1, 2))
        with pytest.raises(ValidationError):
            distance_2d((0, 0), (1, "invalid"))
    
    def test_distance_3d_valid(self):
        # Basic 3D distance
        result = distance_3d((0, 0, 0), (3, 4, 12))
        assert abs(result - 13) < 1e-10  # 3-4-12 triangle
        
        # Same point
        result = distance_3d((1, 1, 1), (1, 1, 1))
        assert result == 0
    
    def test_distance_3d_invalid(self):
        with pytest.raises(ValidationError):
            distance_3d((0, 0), (1, 2, 3))  # 2D point
        with pytest.raises(ValidationError):
            distance_3d((0, 0, 0), (1, 2))  # 2D point

class TestMidpointFunctions:
    def test_midpoint_2d_valid(self):
        result = midpoint_2d((0, 0), (4, 6))
        assert result == (2, 3)
        
        result = midpoint_2d((-2, -4), (2, 4))
        assert result == (0, 0)
    
    def test_midpoint_2d_invalid(self):
        with pytest.raises(ValidationError):
            midpoint_2d((0, 0), (1, 2, 3))
    
    def test_midpoint_3d_valid(self):
        result = midpoint_3d((0, 0, 0), (6, 8, 10))
        assert result == (3, 4, 5)
        
        result = midpoint_3d((-1, -2, -3), (1, 2, 3))
        assert result == (0, 0, 0)
    
    def test_midpoint_3d_invalid(self):
        with pytest.raises(ValidationError):
            midpoint_3d((0, 0), (1, 2, 3))

class TestSlopeFunction:
    def test_slope_valid(self):
        # Positive slope
        result = slope((0, 0), (2, 4))
        assert result == 2
        
        # Negative slope
        result = slope((0, 0), (2, -4))
        assert result == -2
        
        # Zero slope
        result = slope((0, 0), (5, 0))
        assert result == 0
    
    def test_slope_vertical_line(self):
        with pytest.raises(CalculationError):
            slope((0, 0), (0, 5))  # Vertical line
    
    def test_slope_same_point(self):
        with pytest.raises(ValidationError):
            slope((1, 1), (1, 1))

class TestLineEquationFunction:
    def test_line_equation_valid(self):
        # Standard line
        result = line_equation((0, 0), (1, 2))
        assert result["type"] == "linear"
        assert result["slope"] == 2
        assert result["intercept"] == 0
        
        # Line with y-intercept
        result = line_equation((0, 3), (2, 7))
        assert result["type"] == "linear"
        assert result["slope"] == 2
        assert result["intercept"] == 3
    
    def test_line_equation_vertical(self):
        result = line_equation((3, 0), (3, 5))
        assert result["type"] == "vertical"
        assert result["x"] == 3

class TestLineIntersectionFunction:
    def test_line_intersection_valid(self):
        # Two intersecting lines
        result = line_intersection((0, 0), (2, 2), (0, 2), (2, 0))
        assert result == (1, 1)
        
        # Lines intersecting at origin
        result = line_intersection((0, 0), (1, 1), (0, 0), (1, -1))
        assert result == (0, 0)
    
    def test_line_intersection_parallel(self):
        # Parallel lines
        with pytest.raises(CalculationError):
            line_intersection((0, 0), (2, 2), (0, 1), (2, 3))
    
    def test_line_intersection_coincident(self):
        # Same line
        with pytest.raises(CalculationError):
            line_intersection((0, 0), (2, 2), (1, 1), (3, 3))
    
    def test_line_intersection_vertical_lines(self):
        # Two vertical lines
        with pytest.raises(CalculationError):
            line_intersection((1, 0), (1, 5), (2, 0), (2, 5))
        
        # Same vertical line
        with pytest.raises(CalculationError):
            line_intersection((1, 0), (1, 5), (1, 2), (1, 7))
    
    def test_line_intersection_one_vertical(self):
        # One vertical, one normal
        result = line_intersection((2, 0), (2, 5), (0, 1), (4, 3))
        assert result == (2, 2)

class TestPointToLineDistanceFunction:
    def test_point_to_line_distance_valid(self):
        # Point to horizontal line
        result = point_to_line_distance((0, 3), (0, 0), (5, 0))
        assert abs(result - 3) < 1e-10
        
        # Point to vertical line
        result = point_to_line_distance((3, 0), (0, 0), (0, 5))
        assert abs(result - 3) < 1e-10
        
        # Point to diagonal line
        result = point_to_line_distance((0, 0), (1, 1), (2, 0))
        expected = math.sqrt(2)  # Corrected expected value
        assert abs(result - expected) < 1e-10
    
    def test_point_to_line_distance_point_on_line(self):
        # Point on the line
        result = point_to_line_distance((1, 1), (0, 0), (2, 2))
        assert abs(result - 0) < 1e-10
    
    def test_point_to_line_distance_invalid(self):
        with pytest.raises(ValidationError):
            point_to_line_distance((0, 0), (1, 1), (1, 1))  # Same line points

class TestCoordinateValidation:
    def test_coordinate_validation_edge_cases(self):
        # Test with float coordinates
        result = distance_2d((0.5, 0.5), (1.5, 1.5))
        expected = math.sqrt(2)
        assert abs(result - expected) < 1e-10
        
        # Test with negative coordinates
        result = midpoint_2d((-5, -10), (5, 10))
        assert result == (0, 0)
        
        # Test with zero coordinates mixed with non-zero
        # This should raise CalculationError for vertical line
        with pytest.raises(CalculationError):
            slope((0, 0), (0, 5))
