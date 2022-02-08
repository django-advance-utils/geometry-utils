import math
from math import sqrt

from geometry_utils.maths_utility import is_int_or_float, are_ints_or_floats, floats_are_close
from geometry_utils.two_d.vector2 import Vector2


class Vector3:
    """
    A class to create a 3D vector

    Attributes:
    ___________
    x: int/float
        the x-coordinate of the vector
    y: int/float
        the y-coordinate of the vector
    z: int/float
        the z-coordinate of the vector
    w: int/float
        the w-coordinate of the vector
        w=0 leave the vector unchanged when multiplied by a translation matrix

    Methods:
    ________
    __add__(Vector3): Vector3
        Returns the addition of the vector with another 3D vector
    __sub__(Vector3): Vector3
        Returns the subtraction of another 3D vector from the vector
    __mul__(int/float): Vector3
        Returns the multiplication of the vector with an int or float scalar
    __div__(int/float): Vector3
        Returns the division of the vector by an int or float scalar
    __eq__(Vector2): bool
        Returns the equality comparison of the vector with another 3D vector
    __ne__(Vector2): bool
        Returns the inequality comparison of the vector with another 3D vector
    reverse(): Vector3
        Returns the reverse of the vector
    normalise(): Vector3
        Returns the normal of the vector
    length(): int/float
        Returns the pythagorean length of the vector
    dot(Vector3): int/float
        Returns the dot product of vector with another 3D vector
    cross(Vector3): Vector3
        Returns the cross product of vector with another 3D vector
    """
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0):
        if are_ints_or_floats([x, y, z, w]):
            self.x = x
            self.y = y
            self.z = z
            self.w = w
        else:
            raise TypeError("Vector3 argument must be an int or float")

    def __str__(self):
        return ("Vector3(x:" + str("{:.2f}".format(self.x)) +
                ", y:" + str("{:.2f}".format(self.y)) +
                ", z:" + str("{:.2f}".format(self.z)) + ")")

    def __add__(self, other_vector):
        """
        Calculates the addition of vector with another 3D vector

        :param   other_vector: the addition 3D vector
        :type    other_vector: Vector3
        :return: the resulting added vector
        :rtype:  Vector3
        :raises: TypeError: wrong argument type
        """
        if is_vector3(other_vector):
            return Vector3(self.x + other_vector.x, self.y + other_vector.y, self.z + other_vector.z)
        raise TypeError("Addition must be with an object of Vector3")

    def __sub__(self, other_vector):
        """
        Calculates the subtraction of another 3D vector from the vector

        :param   other_vector: the subtraction 3D vector
        :type    other_vector: Vector3
        :return: the resulting subtracted vector
        :rtype:  Vector3
        :raises: TypeError: wrong argument type
        """
        if is_vector3(other_vector):
            return Vector3(self.x - other_vector.x, self.y - other_vector.y, self.z - other_vector.z)
        raise TypeError("Subtraction must be with an object of Vector3")

    def __mul__(self, scalar):
        """
        Calculates the multiplication of self with a scalar.

        :param  scalar: the multiplication scalar
        :type   scalar: int/float
        :return:the resulting multiplied vector
        :rtype: Vector3
        :raises:TypeError: wrong argument type
        """
        if is_int_or_float(scalar):
            return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
        raise TypeError("Multiplication must be by a scalar of type int or float")

    def __div__(self, scalar):
        """
        Calculates the division of self with a scalar.

        :param  scalar: the division scalar
        :type   scalar: int/float
        :return:the resulting divided vector
        :rtype: Vector3
        :raises:TypeError: wrong argument type
        """
        if is_int_or_float(scalar):
            return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
        raise TypeError("Division must be by a scalar of type int or float")

    # division in Python 3.x = division in Python 2.x
    __truediv__ = __div__

    def __eq__(self, other_vector):
        """
        Compares the equality of the vector and another 3D vector.

        :param  other_vector: the other 3D vector
        :type   other_vector: Vector3
        :return:the vector equality
        :rtype: bool
        :raises:TypeError: Wrong argument type
        """
        if is_vector3(other_vector):
            return (floats_are_close(self.x, other_vector.x) and
                    floats_are_close(self.y, other_vector.y) and
                    floats_are_close(self.y, other_vector.y))
        raise TypeError("Comparison must be with another object of Vector3")

    def __ne__(self, other_vector):
        """
        Compares the inequality of the vector and another 3D vector.

        :param  other_vector: the other 3D vector
        :type   other_vector: Vector3
        :return:the vector inequality
        :rtype: bool
        :raises:TypeError: Wrong argument type
        """
        if is_vector3(other_vector):
            return (not floats_are_close(self.x, other_vector.x) or
                    not floats_are_close(self.y, other_vector.y) or
                    not floats_are_close(self.y, other_vector.y))
        raise TypeError("Comparison must be with another object of Vector3")

    def reverse(self):
        """
        Calculates the reverse vector of the vector

        :return: the reverse vector
        :rtype: Vector3
        """
        return Vector3(-self.x, -self.y, -self.z)

    def normalised(self):
        """
        Calculates the normal vector of the vector

        :return: the normal vector
        :rtype: Vector3
        """
        vector_length = self.length()
        if vector_length == 0:
            return self
        return self / vector_length

    def normalise(self):
        vector_length = self.length()
        self.x /= vector_length
        self.y /= vector_length
        self.z /= vector_length
        return self

    def length(self):
        """
        Calculates the pythagorean length of the vector.

        :return: length
        :rtype: int/float
        """
        return sqrt(self.dot(self))

    def dot(self, other_vector):
        """
        Calculates the dot product of self and other vector.

        :param other_vector: the other vector
        :type other_vector: Vector3
        :return: the dot product.
        :rtype: float
        :raises:TypeError: Wrong argument type
        """
        if is_vector3(other_vector):
            return float((self.x * other_vector.x) + (self.y * other_vector.y) + (self.z * other_vector.z))
        raise TypeError("Dot product must be with another object of Vector3")

    def cross(self, other_vector):
        """
        Calculates the cross product of self and other vector.

        :param other_vector: the other vector
        :type other_vector: Vector3
        :return: the cross product.
        :rtype: Vector3
        :raises:TypeError: Wrong argument type
        """
        if is_vector3(other_vector):
            return Vector3(self.y * other_vector.z - self.z * other_vector.y,
                           self.z * other_vector.x - self.x * other_vector.z,
                           self.x * other_vector.y - self.y * other_vector.x)
        raise TypeError("Cross product must be with another object of Vector3")

    def get_perpendicular(self, vector_1, vector_2):
        """
        Calculates the 2D vector perpendicular to the vector

        :return: the perpendicular vector
        :rtype: Vector2
        """
        if self == Vector3():
            return vector_1, vector_2
        x_abs = abs(self.x)
        y_abs = abs(self.y)
        z_abs = abs(self.z)

        cross_vector = Vector3(1.0, 0.0, 0.0)
        if y_abs < x_abs:
            cross_vector.x = 0.0
            cross_vector.y = 1.0
            cross_vector.z = 0.0
        if z_abs < y_abs:
            cross_vector.x = 0.0
            cross_vector.y = 0.0
            cross_vector.z = 1.0

        vector_1 = self.cross(cross_vector).normalised()
        vector_2 = self.cross(vector_1).normalised()

        return vector_1, vector_2

    @classmethod
    def from_comma_string(cls, string):
        v = string.split(',')
        return cls(float(v[0]), float(v[1]), float(v[2]))

    def angle_to(self, other_vector):
        self_unit_vector = self.normalised()
        other_unit_vector = other_vector.normalised()
        dot_product = self_unit_vector.dot(other_unit_vector)
        angle = math.acos(dot_product)
        return angle

    def signed_angle_to(self, other_vector):
        return self.to_vector2().signed_angle_to(other_vector.to_vector2())

    def invert(self):
        self.x *= -1
        self.y *= -1
        self.z *= -1
        return self

    def inverted(self):
        return Vector3(-self.x, -self.y, -self.z)

    def to_vector2(self):
        return Vector2(self.x, self.y)


def is_vector3(input_variable):
    return isinstance(input_variable, Vector3)
