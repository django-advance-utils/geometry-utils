from vector3 import Vector3


class Point3:
    def __init__(self, x, y, z, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, other):
        if isinstance(other, Point3) or isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Point3) or isinstance(other, Vector3):
            return Point3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Point3):
            return bool(self.x == other.x and self.y == other.y and self.z == other.z)

    def __ne__(self, other):
        if isinstance(other, Point3):
            return bool(self.x != other.x or self.y != other.y or self.z != other.z)