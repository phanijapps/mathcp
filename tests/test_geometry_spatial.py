"""Tests for geometry spatial module."""

import pytest
import math
from mathgenius.geometry.spatial import (
    vector_add, vector_subtract, vector_dot_product, vector_cross_product,
    vector_magnitude, vector_normalize, angle_between_vectors,
    rotate_point, translate_point, scale_point
)
from mathgenius.core.errors import ValidationError, CalculationError

class TestVectorOperations:
    def test_vector_add_2d(self):
        result = vector_add((1, 2), (3, 4))
        assert result == (4, 6)
        
        result = vector_add((0, 0), (5, -3))
        assert result == (5, -3)
    
    def test_vector_add_3d(self):
        result = vector_add((1, 2, 3), (4, 5, 6))
        assert result == (5, 7, 9)
        
        result = vector_add((0, 0, 0), (1, -1, 2))
        assert result == (1, -1, 2)
    
    def test_vector_add_dimension_mismatch(self):
        with pytest.raises(ValidationError):
            vector_add((1, 2), (3, 4, 5))
    
    def test_vector_subtract_2d(self):
        result = vector_subtract((5, 7), (2, 3))
        assert result == (3, 4)
        
        result = vector_subtract((0, 0), (1, 1))
        assert result == (-1, -1)
    
    def test_vector_subtract_3d(self):
        result = vector_subtract((10, 8, 6), (4, 3, 2))
        assert result == (6, 5, 4)
    
    def test_vector_dot_product_2d(self):
        result = vector_dot_product((1, 2), (3, 4))
        assert result == 11  # 1*3 + 2*4
        
        result = vector_dot_product((1, 0), (0, 1))
        assert result == 0  # Perpendicular vectors
    
    def test_vector_dot_product_3d(self):
        result = vector_dot_product((1, 2, 3), (4, 5, 6))
        assert result == 32  # 1*4 + 2*5 + 3*6
    
    def test_vector_cross_product_3d(self):
        # i x j = k
        result = vector_cross_product((1, 0, 0), (0, 1, 0))
        assert result == (0, 0, 1)
        
        # j x k = i
        result = vector_cross_product((0, 1, 0), (0, 0, 1))
        assert result == (1, 0, 0)
        
        # k x i = j
        result = vector_cross_product((0, 0, 1), (1, 0, 0))
        assert result == (0, 1, 0)
    
    def test_vector_cross_product_2d_error(self):
        with pytest.raises(ValidationError):
            vector_cross_product((1, 2), (3, 4))  # 2D vectors
    
    def test_vector_magnitude_2d(self):
        result = vector_magnitude((3, 4))
        assert abs(result - 5) < 1e-10
        
        result = vector_magnitude((0, 0))
        assert result == 0
    
    def test_vector_magnitude_3d(self):
        result = vector_magnitude((1, 2, 2))
        assert abs(result - 3) < 1e-10
        
        result = vector_magnitude((0, 0, 0))
        assert result == 0
    
    def test_vector_normalize_2d(self):
        result = vector_normalize((3, 4))
        assert abs(result[0] - 0.6) < 1e-10
        assert abs(result[1] - 0.8) < 1e-10
        
        # Check magnitude is 1
        magnitude = vector_magnitude(result)
        assert abs(magnitude - 1) < 1e-10
    
    def test_vector_normalize_3d(self):
        result = vector_normalize((1, 0, 0))
        assert result == (1, 0, 0)
        
        result = vector_normalize((2, 0, 0))
        assert result == (1, 0, 0)
    
    def test_vector_normalize_zero_vector(self):
        with pytest.raises(ValidationError):
            vector_normalize((0, 0))
        with pytest.raises(ValidationError):
            vector_normalize((0, 0, 0))

class TestAngleBetweenVectors:
    def test_angle_between_vectors_radians(self):
        # Perpendicular vectors
        result = angle_between_vectors((1, 0), (0, 1))
        assert abs(result - math.pi/2) < 1e-10
        
        # Parallel vectors
        result = angle_between_vectors((1, 0), (2, 0))
        assert abs(result - 0) < 1e-10
        
        # Opposite vectors
        result = angle_between_vectors((1, 0), (-1, 0))
        assert abs(result - math.pi) < 1e-10
    
    def test_angle_between_vectors_degrees(self):
        # Perpendicular vectors
        result = angle_between_vectors((1, 0), (0, 1), 'degrees')
        assert abs(result - 90) < 1e-10
        
        # Parallel vectors
        result = angle_between_vectors((1, 0), (2, 0), 'degrees')
        assert abs(result - 0) < 1e-10
        
        # Opposite vectors
        result = angle_between_vectors((1, 0), (-1, 0), 'degrees')
        assert abs(result - 180) < 1e-10
    
    def test_angle_between_vectors_3d(self):
        # Test with 3D vectors
        result = angle_between_vectors((1, 0, 0), (0, 1, 0))
        assert abs(result - math.pi/2) < 1e-10
        
        result = angle_between_vectors((1, 1, 0), (1, -1, 0))
        assert abs(result - math.pi/2) < 1e-10
    
    def test_angle_between_vectors_zero_vector(self):
        with pytest.raises(ValidationError):
            angle_between_vectors((0, 0), (1, 0))
        with pytest.raises(ValidationError):
            angle_between_vectors((1, 0), (0, 0))
    
    def test_angle_between_vectors_invalid_unit(self):
        with pytest.raises(ValidationError):
            angle_between_vectors((1, 0), (0, 1), 'invalid')

class TestGeometricTransformations:
    def test_rotate_point_radians(self):
        # Rotate (1, 0) by 90 degrees counterclockwise
        result = rotate_point((1, 0), math.pi/2)
        assert abs(result[0] - 0) < 1e-10
        assert abs(result[1] - 1) < 1e-10
        
        # Rotate (1, 0) by 180 degrees
        result = rotate_point((1, 0), math.pi)
        assert abs(result[0] - (-1)) < 1e-10
        assert abs(result[1] - 0) < 1e-10
    
    def test_rotate_point_degrees(self):
        # Rotate (1, 0) by 90 degrees counterclockwise
        result = rotate_point((1, 0), 90, unit='degrees')
        assert abs(result[0] - 0) < 1e-10
        assert abs(result[1] - 1) < 1e-10
        
        # Rotate (0, 1) by 90 degrees counterclockwise
        result = rotate_point((0, 1), 90, unit='degrees')
        assert abs(result[0] - (-1)) < 1e-10
        assert abs(result[1] - 0) < 1e-10
    
    def test_rotate_point_around_origin(self):
        # Rotate around different origin
        result = rotate_point((2, 1), 90, origin=(1, 1), unit='degrees')
        assert abs(result[0] - 1) < 1e-10
        assert abs(result[1] - 2) < 1e-10
    
    def test_translate_point_2d(self):
        result = translate_point((1, 2), (3, 4))
        assert result == (4, 6)
        
        result = translate_point((0, 0), (-1, -2))
        assert result == (-1, -2)
    
    def test_translate_point_3d(self):
        result = translate_point((1, 2, 3), (4, 5, 6))
        assert result == (5, 7, 9)
        
        result = translate_point((0, 0, 0), (1, -1, 2))
        assert result == (1, -1, 2)
    
    def test_translate_point_dimension_mismatch(self):
        with pytest.raises(ValidationError):
            translate_point((1, 2), (3, 4, 5))
    
    def test_scale_point_2d(self):
        result = scale_point((2, 4), 2)
        assert result == (4, 8)
        
        result = scale_point((4, 6), 0.5)
        assert result == (2, 3)
    
    def test_scale_point_3d(self):
        result = scale_point((1, 2, 3), 2)
        assert result == (2, 4, 6)
        
        result = scale_point((4, 6, 8), 0.5)
        assert result == (2, 3, 4)
    
    def test_scale_point_from_origin(self):
        # Scale from different origin
        result = scale_point((3, 3), 2, origin=(1, 1))
        assert result == (5, 5)  # (3-1)*2 + 1 = 5
        
        result = scale_point((4, 4), 0.5, origin=(2, 2))
        assert result == (3, 3)  # (4-2)*0.5 + 2 = 3

class TestSpatialValidation:
    def test_invalid_vector_input(self):
        with pytest.raises(ValidationError):
            vector_add("invalid", (1, 2))
        with pytest.raises(ValidationError):
            vector_add((1, 2), [1, 2, 3, 4])  # Too many dimensions
        with pytest.raises(ValidationError):
            vector_add((1, 2), (1,))  # Too few dimensions
    
    def test_invalid_vector_components(self):
        with pytest.raises(ValidationError):
            vector_add((1, "invalid"), (1, 2))
        with pytest.raises(ValidationError):
            vector_magnitude((1, None))
    
    def test_transformation_validation(self):
        with pytest.raises(ValidationError):
            rotate_point((1, 2, 3), 90, unit='degrees')  # 3D point
        with pytest.raises(ValidationError):
            rotate_point((1, 2), 90, unit='invalid')
        with pytest.raises(ValidationError):
            rotate_point((1, 2), "invalid", unit='degrees')
