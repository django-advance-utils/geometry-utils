from three_d.point3 import Point3, is_point3
from three_d.vector3 import Vector3, is_vector3


class AxisAlignedBox3:
    """
    A class to create a 3D box

    Attributes:
    ___________
    min: Point3
        the minimum point in the 3D box
    max: Point3
        the maximum point in the 3D box

    Methods:
    ________
    include(Point3):
        Includes the 3D point in the 3D box
    __contains__(AxisAlignedBox3 or Point3): bool
        Tests if the 3D box contains another 3D box or 3D point
    intersect(AxisAlignedBox3): bool
        Tests if the 3D box intersects another 3D box
    size(): Vector3
        Returns the 3D vector of the 3D box
    offset(Vector3): AxisAlignedBox3
        Returns the 3D box offset by the 3D vector
    centre(): Vector3
        Returns the 3D vector of the centre of the 3D box
    __add__(Vector3): AxisAlignedBox3
        Returns the addition of the 3D box with a 3D vector
    __eq__(AxisAlignedBox3): bool
        Returns the equality comparison of the 3D box with another 3D box
    __ne__(AxisAlignedBox3): bool
        Returns the inequality comparison of the 3D box with another 3D box
    empty(Point3): bool
        Tests if the 3D box is empty
    """

    def __init__(self, minimum=Point3(0.0, 0.0, 0.0), maximum=Point3(0.0, 0.0, 0.0)):
        if is_point3(minimum) and is_point3(maximum):
            self.min = minimum
            self.max = maximum
        else:
            raise TypeError("AxisAlignedBox3 arguments must be objects of Point3")

    def include(self, other):
        if is_point3(other):
            self.max.x = max(self.max.x, other.x)
            self.min.x = min(self.min.x, other.x)
            self.max.y = max(self.max.y, other.y)
            self.min.y = min(self.min.y, other.y)
            self.max.z = max(self.max.z, other.z)
            self.min.z = min(self.min.z, other.z)
        elif is_box3(other):
            self.include(other.min)
            self.include(other.max)
        else:
            raise TypeError("Inclusion must be with an object of Point3 or AxisAlignedBox3")

    def __contains__(self, item):
        """
        Test the 3D point or 3D box is in self

        :param  item: the other 3D point or 3D box
        :type   item: Point3/AxisAlignedBox3
        :return:the item inclusion
        :rtype: bool
        :raises:TypeError: wrong argument type
        """
        if is_point3(item):
            return self.min <= item <= self.max
        if isinstance(item, AxisAlignedBox3):
            return self.__contains__(item.min) and self.__contains__(item.max)
        raise TypeError("Variable must be an object of Point2 or AxisAlignedBox2")

    def intersects(self, item):
        """
        Test self intersects the other 3D box

        :param  item: the other 3D box
        :type   item: AxisAlignedBox3
        :return:the item intersection
        :rtype: bool
        :raises:TypeError: wrong argument type
        """
        if is_box3(item):
            return item.min >= self.min and item.max <= self.max
        raise TypeError("Intersection must be with an object of AxisAlignedBox2")

    def size(self):
        """
        Calculates the 3D vector size of self

        :return:the 3D box size
        :rtype: Vector3
        """
        return (self.max - self.min).to_vector()

    def offset(self, offset_vector):
        """
        Offsets self by 3D vector

        :param  offset_vector: the other 3D vector
        :type   offset_vector: Vector3
        :return:the offset box
        :rtype: AxisAlignedBox3
        :raises:TypeError: wrong argument type
        """
        if is_vector3(offset_vector):
            return self + offset_vector
        raise TypeError("Offset must be with an object of Vector3")

    def centre(self):
        """
        Calculates the centre of self

        :return:the box centre
        :rtype: Vector3
        """
        return ((self.min + self.max).to_vector())/2.0

    def __add__(self, vector):
        """
        Calculates the addition of self with a vector

        :param  vector: the addition vector
        :type   vector: Vector3
        :return:the resulting added box
        :rtype: AxisAlignedBox3
        :raises:TypeError: wrong argument type
        """
        if is_vector3(vector):
            return AxisAlignedBox3(self.min + vector, self.max + vector)
        raise TypeError("Addition must be with an object of Vector3")

    def __eq__(self, box):
        """
        Compares the equality of self and other box

        :param  box: the other 3D box
        :type   box: AxisAlignedBox3
        :return:the box equality
        :rtype: bool
        :raises:TypeError: Wrong argument type
        """
        if is_box3(box):
            return self.max == box.max and self.min == box.min

    def __ne__(self, box):
        """
        Compares the inequality of self with another vector.

        :param  box: the other 3D box
        :type   box: AxisAlignedBox3
        :return:the box inequality
        :rtype: bool
        :raises:TypeError: Wrong argument type
        """
        if is_box3(box):
            return self.max != box.max or self.min != box.min
        raise TypeError("Comparison must be with an object of AxisAlignedBox3")

    def empty(self):
        """
        Checks if self is empty

        :return:the emptiness of the box
        :rtype: bool
        """
        return self.size() == Vector3(0.0, 0.0, 0.0)


def is_box3(input_variable):
    return isinstance(input_variable, AxisAlignedBox3)