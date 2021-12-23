import pytest
from math import sqrt

from geometry_utils.three_d.vector3 import Vector3

'''
Vector Addition Tests
'''


def test_vector3_vector3_addition_return_type(test_vector3_1, test_vector3_2):
    assert isinstance(test_vector3_1 + test_vector3_2, Vector3)


def test_vector3_float_addition(test_vector3_1):
    with pytest.raises(TypeError):
        return test_vector3_1 + 9.0


def test_vector3_vector3_addition_arithmetic(test_vector3_1, test_vector3_2):
    assert test_vector3_1 + test_vector3_2 == Vector3(2.0, 1.0, 1.0)


'''
Vector Subtraction Tests
'''


def test_vector3_vector3_subtraction_return_type(test_vector3_1, test_vector3_2):
    assert isinstance(test_vector3_1 - test_vector3_2, Vector3)


def test_vector3_float_subtraction(test_vector3_1):
    with pytest.raises(TypeError):
        return test_vector3_1 - 9.0


def test_vector3_vector3_subtraction_arithmetic(test_vector3_1, test_vector3_2):
    assert test_vector3_1 - test_vector3_2 == Vector3(0.0, 1.0, 1.0)


'''
Vector Multiplication Tests
'''


def test_vector3_vector3_multiplication(test_vector3_1, test_vector3_2):
    with pytest.raises(TypeError):
        return test_vector3_1 * test_vector3_2


def test_vector3_float_multiplication_return_type(test_vector3_1, test_vector3_2):
    assert isinstance(test_vector3_1 * 9.0, Vector3)


def test_vector_float_multiplication_arithmetic(test_vector3_1):
    assert test_vector3_1 * 2.0 == Vector3(2.0, 2.0, 2.0)


'''
Vector Division Tests
'''


def test_vector3_vector3_division(test_vector3_1, test_vector3_2):
    with pytest.raises(TypeError):
        return test_vector3_1 / test_vector3_2


def test_vector3_float_division(test_vector3_1):
    assert test_vector3_1 / 2.0 == Vector3(0.5, 0.5, 0.5)


def test_vector3_float_division_return_type(test_vector3_1):
    assert isinstance((test_vector3_1 / 9.0), Vector3)


'''
Vector Equality and Inequality Tests
'''


def test_vector3_vector3_equality(test_vector3_1, test_vector3_3):
    assert test_vector3_1 == test_vector3_1
    assert test_vector3_1 == test_vector3_3


def test_vector3_vector3_inequality(test_vector3_1, test_vector3_2):
    assert test_vector3_1 != test_vector3_2
    assert not (test_vector3_1 == test_vector3_2)


'''
Vector Dot and Cross Tests
'''


def test_vector3_dot_vector3_return_type(test_vector3_1, test_vector3_2):
    assert isinstance(test_vector3_1.dot(test_vector3_2), float)
    assert isinstance(test_vector3_2.dot(test_vector3_1), float)


def test_vector3_dot_vector3_arithmetic(test_vector3_1, test_vector3_2):
    assert test_vector3_1.dot(test_vector3_2) == 1.0
    assert test_vector3_2.dot(test_vector3_1) == 1.0


def test_vector3_cross_vector3_return_type(test_vector3_1, test_vector3_2):
    assert isinstance(test_vector3_1.cross(test_vector3_2), Vector3)
    assert isinstance(test_vector3_2.cross(test_vector3_1), Vector3)


def test_vector3_cross_vector3_arithmetic(test_vector3_1, test_vector3_2):
    assert test_vector3_1.cross(test_vector3_2) == Vector3(0.0, 1.0, -1.0)
    assert test_vector3_2.cross(test_vector3_1) == Vector3(0.0, -1.0, 1.0)


'''
Vector Length and Normalise Tests
'''


def test_vector3_length_return_type(test_vector3_1):
    assert isinstance(test_vector3_1.length(), float)


def test_vector3_length_arithmetic(test_vector3_1):
    assert test_vector3_1.length() == sqrt(3.0)


def test_vector3_normalised_return_type(test_vector3_1):
    assert isinstance(test_vector3_1.normalised(), Vector3)


def test_vector3_normalised_arithmetic(test_vector3_1, test_vector3_4):
    assert test_vector3_1.normalised() == Vector3(1 / sqrt(3), 1 / sqrt(3), 1 / sqrt(3))
    assert test_vector3_4.normalised() == test_vector3_4


'''
Vector Reverse Tests
'''


def test_reversed_vector3_return_type(test_vector3_1):
    assert isinstance(test_vector3_1, Vector3)


def test_reversed_vector3_arithmetic(test_vector3_1, test_vector3_4):
    assert test_vector3_1.reverse() == Vector3(-1.0, -1.0, -1.0)
    assert test_vector3_4.reverse() == test_vector3_4
