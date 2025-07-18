"""Integration tests for geometry modules in API layer."""

import pytest
import math
from mathgenius.api.dispatcher import (
    # Shapes
    triangle_area, circle_area, rectangle_area, sphere_volume,
    # Trigonometry
    sin, cos, tan, degrees_to_radians,
    # Coordinates
    distance_2d, midpoint_2d, slope, line_intersection,
    # Spatial
    vector_add, vector_dot_product, angle_between_vectors
)
from mathgenius.core.errors import ValidationError, CalculationError

class TestAPIIntegration:
    def test_geometry_shapes_api(self):
        """Test that shape functions are accessible through API."""
        # Test triangle area
        assert triangle_area(3, 4) == 6.0
        
        # Test circle area
        result = circle_area(2)
        assert abs(result - 4 * math.pi) < 1e-10
        
        # Test rectangle area
        assert rectangle_area(5, 3) == 15
        
        # Test sphere volume
        result = sphere_volume(2)
        expected = (4/3) * math.pi * 8
        assert abs(result - expected) < 1e-10
    
    def test_geometry_trigonometry_api(self):
        """Test that trigonometry functions are accessible through API."""
        # Test sin
        assert abs(sin(math.pi/2) - 1) < 1e-10
        
        # Test cos
        assert abs(cos(0) - 1) < 1e-10
        
        # Test tan
        assert abs(tan(math.pi/4) - 1) < 1e-10
        
        # Test angle conversion
        result = degrees_to_radians(180)
        assert abs(result - math.pi) < 1e-10
    
    def test_geometry_coordinates_api(self):
        """Test that coordinate functions are accessible through API."""
        # Test distance
        result = distance_2d((0, 0), (3, 4))
        assert abs(result - 5) < 1e-10
        
        # Test midpoint
        result = midpoint_2d((0, 0), (4, 6))
        assert result == (2, 3)
        
        # Test slope
        result = slope((0, 0), (2, 4))
        assert result == 2
        
        # Test line intersection
        result = line_intersection((0, 0), (2, 2), (0, 2), (2, 0))
        assert result == (1, 1)
    
    def test_geometry_spatial_api(self):
        """Test that spatial functions are accessible through API."""
        # Test vector addition
        result = vector_add((1, 2), (3, 4))
        assert result == (4, 6)
        
        # Test dot product
        result = vector_dot_product((1, 2), (3, 4))
        assert result == 11
        
        # Test angle between vectors
        result = angle_between_vectors((1, 0), (0, 1))
        assert abs(result - math.pi/2) < 1e-10
    
    def test_backward_compatibility(self):
        """Test that existing Story 1 functions still work."""
        # These should be available from the previous implementation
        from mathgenius.api.dispatcher import add, subtract, multiply, divide
        
        assert add(2, 3) == 5
        assert subtract(5, 3) == 2
        assert multiply(4, 3) == 12
        assert divide(10, 2) == 5
    
    def test_error_handling_consistency(self):
        """Test that error handling is consistent across modules."""
        # Test validation errors
        with pytest.raises(ValidationError):
            triangle_area("invalid", 4)
        
        with pytest.raises(ValidationError):
            sin("invalid")
        
        with pytest.raises(ValidationError):
            distance_2d("invalid", (1, 2))
        
        with pytest.raises(ValidationError):
            vector_add("invalid", (1, 2))
        
        # Test calculation errors
        with pytest.raises(CalculationError):
            tan(90, 'degrees')  # Undefined

class TestComplexGeometryOperations:
    def test_combined_operations(self):
        """Test combining multiple geometry operations."""
        # Calculate area of triangle using coordinates
        p1 = (0, 0)
        p2 = (3, 0)
        p3 = (0, 4)
        
        # Get side lengths
        side1 = distance_2d(p1, p2)  # 3
        side2 = distance_2d(p2, p3)  # 5
        side3 = distance_2d(p3, p1)  # 4
        
        # Calculate area using base and height
        area = triangle_area(side1, 4)  # base=3, height=4
        assert area == 6.0
    
    def test_trigonometry_with_coordinates(self):
        """Test trigonometry combined with coordinate geometry."""
        # Create a right triangle
        p1 = (0, 0)
        p2 = (3, 0)
        p3 = (0, 4)
        
        # Calculate hypotenuse
        hypotenuse = distance_2d(p2, p3)
        assert abs(hypotenuse - 5) < 1e-10
        
        # Calculate angle using trigonometry
        angle = math.asin(4/5)  # sin(angle) = opposite/hypotenuse
        sin_result = sin(angle)
        assert abs(sin_result - 0.8) < 1e-10
    
    def test_vector_operations_with_coordinates(self):
        """Test vector operations with coordinate geometry."""
        # Create vectors from coordinates
        p1 = (1, 2)
        p2 = (4, 6)
        
        # Vector from p1 to p2
        vector = vector_add(p2, vector_add(p1, (-p1[0], -p1[1])))
        # This should be equivalent to (p2[0] - p1[0], p2[1] - p1[1])
        expected = (3, 4)
        
        # Test vector magnitude equals distance
        magnitude = math.sqrt(vector_dot_product(expected, expected))
        distance = distance_2d(p1, p2)
        assert abs(magnitude - distance) < 1e-10

class TestGeometryDocumentation:
    def test_function_docstrings(self):
        """Test that all functions have proper docstrings."""
        functions_to_test = [
            triangle_area, circle_area, sin, cos, 
            distance_2d, vector_add, angle_between_vectors
        ]
        
        for func in functions_to_test:
            assert func.__doc__ is not None
            assert len(func.__doc__.strip()) > 0
    
    def test_module_imports(self):
        """Test that all modules can be imported correctly."""
        import mathgenius.geometry.shapes
        import mathgenius.geometry.trigonometry
        import mathgenius.geometry.coordinates
        import mathgenius.geometry.spatial
        
        # Test that main geometry module works
        import mathgenius.geometry
        
        # Test that functions are available in geometry module
        assert hasattr(mathgenius.geometry, 'triangle_area')
        assert hasattr(mathgenius.geometry, 'sin')
        assert hasattr(mathgenius.geometry, 'distance_2d')
        assert hasattr(mathgenius.geometry, 'vector_add')
