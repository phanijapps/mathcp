import pytest
from mathgenius.arithmetic.operations import add, subtract, multiply, divide, power, modulo
from mathgenius.core.errors import ValidationError, CalculationError

def test_add():
    assert add(2, 3) == 5
    with pytest.raises(ValidationError):
        add(2, "a")

def test_subtract():
    assert subtract(5, 2) == 3
    with pytest.raises(ValidationError):
        subtract("x", 2)

def test_multiply():
    assert multiply(4, 3) == 12
    with pytest.raises(ValidationError):
        multiply(4, None)

def test_divide():
    assert divide(10, 2) == 5
    with pytest.raises(CalculationError):
        divide(1, 0)
    with pytest.raises(ValidationError):
        divide("a", 1)

def test_power():
    assert power(2, 3) == 8
    with pytest.raises(ValidationError):
        power(2, "b")

def test_modulo():
    assert modulo(10, 3) == 1
    with pytest.raises(CalculationError):
        modulo(1, 0)
    with pytest.raises(ValidationError):
        modulo("a", 2)
