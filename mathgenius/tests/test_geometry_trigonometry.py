"""Tests for geometry trigonometry module."""

import pytest
import math
from mathgenius.geometry.trigonometry import (
    sin, cos, tan, asin, acos, atan,
    sinh, cosh, tanh,
    degrees_to_radians, radians_to_degrees
)
from mathgenius.core.errors import ValidationError, CalculationError

class TestAngleConversion:
    def test_degrees_to_radians_valid(self):
        result = degrees_to_radians(180)
        assert abs(result - math.pi) < 1e-10
        
        result = degrees_to_radians(90)
        assert abs(result - math.pi/2) < 1e-10
        
        result = degrees_to_radians(0)
        assert result == 0
    
    def test_radians_to_degrees_valid(self):
        result = radians_to_degrees(math.pi)
        assert abs(result - 180) < 1e-10
        
        result = radians_to_degrees(math.pi/2)
        assert abs(result - 90) < 1e-10
        
        result = radians_to_degrees(0)
        assert result == 0
    
    def test_conversion_invalid_input(self):
        with pytest.raises(ValidationError):
            degrees_to_radians("180")
        with pytest.raises(ValidationError):
            radians_to_degrees("pi")

class TestBasicTrigFunctions:
    def test_sin_radians(self):
        assert abs(sin(0) - 0) < 1e-10
        assert abs(sin(math.pi/2) - 1) < 1e-10
        assert abs(sin(math.pi) - 0) < 1e-10
        assert abs(sin(3*math.pi/2) - (-1)) < 1e-10
    
    def test_sin_degrees(self):
        assert abs(sin(0, 'degrees') - 0) < 1e-10
        assert abs(sin(90, 'degrees') - 1) < 1e-10
        assert abs(sin(180, 'degrees') - 0) < 1e-10
        assert abs(sin(270, 'degrees') - (-1)) < 1e-10
    
    def test_cos_radians(self):
        assert abs(cos(0) - 1) < 1e-10
        assert abs(cos(math.pi/2) - 0) < 1e-10
        assert abs(cos(math.pi) - (-1)) < 1e-10
        assert abs(cos(3*math.pi/2) - 0) < 1e-10
    
    def test_cos_degrees(self):
        assert abs(cos(0, 'degrees') - 1) < 1e-10
        assert abs(cos(90, 'degrees') - 0) < 1e-10
        assert abs(cos(180, 'degrees') - (-1)) < 1e-10
        assert abs(cos(270, 'degrees') - 0) < 1e-10
    
    def test_tan_radians(self):
        assert abs(tan(0) - 0) < 1e-10
        assert abs(tan(math.pi/4) - 1) < 1e-10
        assert abs(tan(math.pi) - 0) < 1e-10
    
    def test_tan_degrees(self):
        assert abs(tan(0, 'degrees') - 0) < 1e-10
        assert abs(tan(45, 'degrees') - 1) < 1e-10
        assert abs(tan(180, 'degrees') - 0) < 1e-10
    
    def test_tan_undefined(self):
        with pytest.raises(CalculationError):
            tan(90, 'degrees')
        with pytest.raises(CalculationError):
            tan(270, 'degrees')
    
    def test_trig_invalid_unit(self):
        with pytest.raises(ValidationError):
            sin(0, 'invalid')
        with pytest.raises(ValidationError):
            cos(0, 'invalid')
        with pytest.raises(ValidationError):
            tan(0, 'invalid')

class TestInverseTrigFunctions:
    def test_asin_radians(self):
        assert abs(asin(0) - 0) < 1e-10
        assert abs(asin(1) - math.pi/2) < 1e-10
        assert abs(asin(-1) - (-math.pi/2)) < 1e-10
    
    def test_asin_degrees(self):
        assert abs(asin(0, 'degrees') - 0) < 1e-10
        assert abs(asin(1, 'degrees') - 90) < 1e-10
        assert abs(asin(-1, 'degrees') - (-90)) < 1e-10
    
    def test_acos_radians(self):
        assert abs(acos(1) - 0) < 1e-10
        assert abs(acos(0) - math.pi/2) < 1e-10
        assert abs(acos(-1) - math.pi) < 1e-10
    
    def test_acos_degrees(self):
        assert abs(acos(1, 'degrees') - 0) < 1e-10
        assert abs(acos(0, 'degrees') - 90) < 1e-10
        assert abs(acos(-1, 'degrees') - 180) < 1e-10
    
    def test_atan_radians(self):
        assert abs(atan(0) - 0) < 1e-10
        assert abs(atan(1) - math.pi/4) < 1e-10
        assert abs(atan(-1) - (-math.pi/4)) < 1e-10
    
    def test_atan_degrees(self):
        assert abs(atan(0, 'degrees') - 0) < 1e-10
        assert abs(atan(1, 'degrees') - 45) < 1e-10
        assert abs(atan(-1, 'degrees') - (-45)) < 1e-10
    
    def test_inverse_trig_domain_errors(self):
        with pytest.raises(ValidationError):
            asin(2)
        with pytest.raises(ValidationError):
            asin(-2)
        with pytest.raises(ValidationError):
            acos(2)
        with pytest.raises(ValidationError):
            acos(-2)
    
    def test_inverse_trig_invalid_unit(self):
        with pytest.raises(ValidationError):
            asin(0, 'invalid')
        with pytest.raises(ValidationError):
            acos(0, 'invalid')
        with pytest.raises(ValidationError):
            atan(0, 'invalid')

class TestHyperbolicFunctions:
    def test_sinh_valid(self):
        assert abs(sinh(0) - 0) < 1e-10
        assert abs(sinh(1) - math.sinh(1)) < 1e-10
        assert abs(sinh(-1) - math.sinh(-1)) < 1e-10
    
    def test_cosh_valid(self):
        assert abs(cosh(0) - 1) < 1e-10
        assert abs(cosh(1) - math.cosh(1)) < 1e-10
        assert abs(cosh(-1) - math.cosh(-1)) < 1e-10
    
    def test_tanh_valid(self):
        assert abs(tanh(0) - 0) < 1e-10
        assert abs(tanh(1) - math.tanh(1)) < 1e-10
        assert abs(tanh(-1) - math.tanh(-1)) < 1e-10
    
    def test_hyperbolic_invalid_input(self):
        with pytest.raises(ValidationError):
            sinh("0")
        with pytest.raises(ValidationError):
            cosh("0")
        with pytest.raises(ValidationError):
            tanh("0")

class TestTrigonometricIdentities:
    def test_pythagorean_identity(self):
        """Test sin²(x) + cos²(x) = 1"""
        angles = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2]
        for angle in angles:
            sin_val = sin(angle)
            cos_val = cos(angle)
            assert abs(sin_val**2 + cos_val**2 - 1) < 1e-10
    
    def test_tan_identity(self):
        """Test tan(x) = sin(x)/cos(x)"""
        angles = [0, math.pi/6, math.pi/4, math.pi/3]
        for angle in angles:
            tan_val = tan(angle)
            sin_val = sin(angle)
            cos_val = cos(angle)
            assert abs(tan_val - sin_val/cos_val) < 1e-10
