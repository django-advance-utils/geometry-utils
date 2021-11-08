from three_d.axis_aligned_box3 import AxisAlignedBox3
from three_d.point3 import Point3


class Edge3:
    def __init__(self,
                 p1=Point3(0.0, 0.0, 0.0),
                 p2=Point3(0.0, 0.0, 0.0),
                 via=Point3(0.0, 0.0, 0.0),
                 radius=0.0,
                 clockwise=False,
                 large=False):
        if isinstance(p1, Point3) and isinstance(p2, Point3):
            self.p1 = p1
            self.p2 = p2
            self.via = via
            self.radius = radius
            self.clockwise = clockwise
            self.large = large
            self.arc_centre = self.get_arc_centre()

    def point_parametric(self, s):
        if isinstance(s, float):
            if self.p1 == self.p2:
                return self.p1

            tangent = self.get_tangent()  # vector
            p1_p2_distance = self.p1.distance_to(self.p2)  # vector
            vector = tangent * (s * p1_p2_distance)  # vector
            return self.p1 + vector  # point

    def parametric_point(self, point):
        if isinstance(point, Point3):
            tangent = self.get_tangent()  # vector
            point_p1_difference = (point - self.p1).to_vector()  # vector
            distance = tangent.dot(point_p1_difference)
            return distance / self.p1.distance_to(self.p2)

    def get_arc_centre(self):
        if self.radius == 0.0:
            return (self.p1 + self.p2) * 0.5

    def get_tangent(self):
        p1_vector = self.p1.to_vector()
        p2_vector = self.p2.to_vector()
        return (p2_vector - p1_vector).normalise()

    def get_edge_bounds(self):
        bounds = AxisAlignedBox3()
        bounds.include(self.p1)
        bounds.include(self.p2)
        return bounds