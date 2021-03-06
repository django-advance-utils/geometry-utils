import pytest

from geometry_utils.two_d.axis_aligned_box2 import AxisAlignedBox2
from geometry_utils.two_d.point2 import Point2
from geometry_utils.two_d.vector2 import Vector2


def test_box2_with_string_inputs():
    with pytest.raises(TypeError):
        return AxisAlignedBox2("0", "0")


def test_box2_print_string(test_box2_2):
    assert test_box2_2.__str__() == "AxisAlignedBox2(min:Point2(x:0.00, y:0.00), max:Point2(x:0.00, y:0.00))"


def test_box2_box2_addition_return_arithmetic(test_box2_1, test_box2_2):
    with pytest.raises(TypeError):
        return test_box2_1 + test_box2_2


def test_box2_vector2_addition_return_type(test_box2_1, test_vector2_1):
    assert isinstance(test_box2_1 + test_vector2_1, AxisAlignedBox2)


def test_box2_vector2_addition_arithmetic(test_box2_1, test_vector2_1):
    assert test_box2_1 + test_vector2_1 == AxisAlignedBox2(Point2(1.0, 1.0), Point2(3.0, 3.0))


def test_box2_contains_point2(test_box2_1, test_point2_1, test_point2_2):
    assert test_point2_1 in test_box2_1
    assert test_point2_2 in test_box2_1


def test_box2_does_not_contain_point2(test_box2_2, test_point2_2):
    assert test_point2_2 not in test_box2_2


def test_box2_includes_point2(test_box2_3, test_point2_3):
    test_box2_3.include(test_point2_3)
    assert test_box2_3.min == Point2(0.0, 0.0) and test_box2_3.max == Point2(1.0, 1.0)


def test_box2_invalid_includes_edge2(test_edge2_1):
    test_box = AxisAlignedBox2()
    test_box.include(test_edge2_1)
    assert test_box.min == Point2(0.0, 0.0) and test_box.max == Point2(0.0, 0.0)


def test_box2_includes_edge2(test_edge2_3):
    test_box = AxisAlignedBox2(Point2(0.0, 0.0), Point2(0.0, 0.0))
    test_box.include(test_edge2_3)
    assert test_box.min == Point2(0.0, 0.0) and test_box.max == Point2(4.0, 4.0)


def test_box2_contains_box2(test_box2_1, test_box2_3):
    assert test_box2_3 in test_box2_1
    assert test_box2_3 in test_box2_1


def test_box2_does_not_contain_box2(test_box2_1, test_box2_3):
    assert test_box2_1 not in test_box2_3
    assert test_box2_1 not in test_box2_3


def test_box2_contain_float(test_box2_1):
    with pytest.raises(TypeError):
        return 9.0 in test_box2_1


def test_box2_include_box2(test_box2_1, test_box2_3):
    test_box2_3.include(test_box2_1)
    assert test_box2_3.min == Point2(0.0, 0.0) and test_box2_3.max == Point2(2.0, 2.0)


def test_box2_include_float(test_box2_1):
    with pytest.raises(TypeError):
        return test_box2_1.include(9.0)


def test_box2_intersects_box2(test_box2_1, test_box2_2, test_box2_3):
    assert test_box2_1.intersects(test_box2_2)
    assert test_box2_1.intersects(test_box2_3)


def test_box2_intersects_float(test_box2_1):
    with pytest.raises(TypeError):
        return test_box2_1.intersects(9.0)


def test_box2_size(test_box2_1):
    assert test_box2_1.size() == Vector2(2.0, 2.0)


def test_box2_offset_by_vector2(test_box2_1, test_vector2_1):
    assert test_box2_1.offset(test_vector2_1) == AxisAlignedBox2(Point2(1.0, 1.0), Point2(3.0, 3.0))


def test_box2_offset_by_float(test_box2_1):
    with pytest.raises(TypeError):
        return test_box2_1.offset(9.0)


def test_box2_centre(test_box2_1):
    assert test_box2_1.centre() == Point2(1.0, 1.0)


def test_box2_equals_box2(test_box2_1, test_box2_2, test_box2_4):
    assert test_box2_1 == test_box2_1
    assert test_box2_2 == test_box2_4


def test_box2_equals_float(test_box2_1):
    with pytest.raises(TypeError):
        return test_box2_1 == 9.0


def test_box2_not_equals_box2(test_box2_1, test_box2_2):
    assert test_box2_1 != test_box2_2


def test_box2_not_equals_float(test_box2_1):
    with pytest.raises(TypeError):
        return test_box2_1 != 9.0


def test_box2_is_empty(test_box2_4):
    assert test_box2_4.is_empty()


def test_box2_invalid_is_empty():
    test_box = AxisAlignedBox2()
    assert test_box.is_empty()


def test_box2_to_axis_aligned_box3(test_box2_2, test_box3_2):
    assert test_box2_2.to_axis_aligned_box3() == test_box3_2


def test_box2_invalid_to_axis_aligned_box3(test_box2_5, test_box3_5):
    assert test_box2_5.to_axis_aligned_box3() == test_box3_5
