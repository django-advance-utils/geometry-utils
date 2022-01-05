import copy
from copy import deepcopy

from geometry_utils.maths_utility import is_int_or_float, is_list
from geometry_utils.two_d.axis_aligned_box2 import AxisAlignedBox2
from geometry_utils.two_d.edge2 import Edge2
from geometry_utils.two_d.vector2 import is_vector2, Vector2
from geometry_utils.two_d.point2 import Point2


class Path2:
    """
    A class to create a 2D path

    Attributes:
    ___________
    list_of_edges: list
        the list of 2D edges to establish a path
    first_edge: Edge2
        the first 2D edge on the path
    last_edge: Edge2
        the last 2D edge on the path

    Methods:
    ________
    is_closed(): bool
        Returns the result of the tests if the path is closed
    is_continuous(): bool
        Returns the result of the tests if the path is continuous
    get_path_bounds(): AxisAlignedBox2()
        Returns 2D box containing the edges of the path
    """

    def __init__(self):
        self.list_of_edges = []

    def __str__(self):
        self.print_edges()
        return ""

    def print_edges(self):
        print "Path2(list of edges: "
        for index, edge in enumerate(self.list_of_edges):
            print ("\t" + str(index) + "\t" + str(edge))
        print ")"

    def __eq__(self, other_path):
        if is_path2(other_path) and self.path_length == other_path.path_length:
            for index in range(self.path_length):
                if self.list_of_edges[index] != other_path.list_of_edges[index]:
                    return False
            return True
        else:
            if not is_path2(other_path):
                raise TypeError("Comparison must be done with another object of Path2")
            if self.path_length != other_path.path_length:
                raise IndexError("Comparison must be done with another path of equal number of edges")

    @property
    def get_first_edge(self):
        if self.path_length >= 1:
            return self.list_of_edges[0]
        raise IndexError("Can not find the first edge of an empty list of edges")

    @property
    def get_last_edge(self):
        if self.path_length >= 1:
            return self.list_of_edges[-1]
        raise IndexError("Can not find the last edge of an empty list of edges")

    @property
    def path_length(self):
        """
        Calculates the number of Edge2 edges in the path

        :return: number of edges in the path
        :rtype: int
        """
        return len(self.list_of_edges)

    @property
    def is_closed(self):
        """
        Tests if the path is closed

        :return: closeness of the path
        :rtype:  bool
        """
        if self.path_length > 2:
            return self.list_of_edges[-1].p2 == self.list_of_edges[0].p1 and self.is_continuous
        return False

    @property
    def is_continuous(self):
        """
        Tests if the path is continuous

        :return:continuity of the path
        :rtype: bool
        """
        continuity = True

        if self.path_length < 2:
            continuity = False
        else:
            for edge, next_edge in zip(self.list_of_edges, self.list_of_edges[1:]):
                if edge.p2 != next_edge.p1:
                    continuity = False
        return continuity

    @property
    def get_bounds(self):
        """
        Derives the AxisAlignedBox2 containing the bounds of the path

        :return:the box containing the path bounds
        :rtype: AxisAlignedBox2
        """
        path_bounds = AxisAlignedBox2()
        for edge in self.list_of_edges:
            path_bounds.include(edge.get_edge_bounds())

            if edge.is_arc():
                positive_x = edge.centre + Vector2(edge.radius, 0)
                positive_y = edge.centre + Vector2(0, edge.radius)
                negative_x = edge.centre + Vector2(-edge.radius, 0)
                negative_y = edge.centre + Vector2(0, -edge.radius)

                parametric_positive_x = edge.parametric_point(positive_x)
                parametric_positive_y = edge.parametric_point(positive_y)
                parametric_negative_x = edge.parametric_point(negative_x)
                parametric_negative_y = edge.parametric_point(negative_y)

                lower_bound = -0.0001
                upper_bound = 1.0001

                if lower_bound < parametric_positive_x < upper_bound:
                    path_bounds.include(positive_x)
                if lower_bound < parametric_positive_y < upper_bound:
                    path_bounds.include(positive_y)
                if lower_bound < parametric_negative_x < upper_bound:
                    path_bounds.include(negative_x)
                if lower_bound < parametric_negative_y < upper_bound:
                    path_bounds.include(negative_y)

        return path_bounds

    def to_tuple_list(self):
        path_tuple_list = []
        for edge in self.list_of_edges:
            path_tuple_list.append((edge.p1, edge.p2))
        return path_tuple_list

    def remove_duplicate_edges(self):
        indices_of_edges_to_remove = []
        last_edge = None

        for index, edge in enumerate(self.list_of_edges):
            if last_edge is not None:
                if edge == last_edge:
                    indices_of_edges_to_remove.append(index)
            last_edge = edge

        indices_of_edges_to_remove.sort(reverse=True)
        for index in indices_of_edges_to_remove:
            del self.list_of_edges[index]
        return self

    def mirror_y(self):
        for edge in self.list_of_edges:
            edge.mirror_y()
        return self

    def offset_path(self, vector):
        if is_vector2(vector):
            for edge in self.list_of_edges:
                edge.offset_edge(vector)
            return self
        else:
            raise TypeError("Path offset must be done with a vector")

    def rotate_around(self, rotation_vector, rotation_angle):
        if is_vector2(rotation_vector) and is_int_or_float(rotation_angle):
            reversed_rotation_vector = rotation_vector.reverse()
            self.offset_path(reversed_rotation_vector)
            self.rotate(rotation_angle)
            self.offset_path(rotation_vector)
        return self

    def rotate(self, rotation_angle):
        for edge in self.list_of_edges:
            edge.rotate(rotation_angle)
        return self

    def close_path(self):
        if self.path_length > 1 and not self.is_closed:
            if not self.is_continuous:
                for index, edge in enumerate(self.list_of_edges):
                    if index == 0:
                        continue
                    if self.list_of_edges[index - 1].p2 != edge.p1:
                        self.list_of_edges.insert(index, Edge2(self.list_of_edges[index - 1].p2, edge.p1))
                        index += 1
            self.list_of_edges.append(Edge2(deepcopy(self.list_of_edges[-1].p2), deepcopy(self.list_of_edges[0].p1)))
        return self

    def is_circle(self):
        return self.path_length == 1 and self.list_of_edges[0].is_circle()

    def get_enclosed_area(self):
        path = deepcopy(self)

        path.remove_duplicate_edges()
        if path.is_closed and path.path_length != 0:
            return path
        raise TypeError("The path must be closed and have more than one edge")

    def remove_arcs(self):
        index = 0
        list_of_edges_to_remove = []
        for edge in self.list_of_edges:
            if edge.is_arc():
                list_of_edges_to_remove.append((index, edge.flatten_arc()))
                edge.radius = 0
                edge.clockwise = False
                edge.large = False
            index += 1

        index_offset = 0
        for new_edge in list_of_edges_to_remove:
            offset_location = new_edge[0] + index_offset
            del self.list_of_edges[offset_location]
            self.list_of_edges[offset_location:offset_location] = new_edge[1]
            index_offset += len(new_edge[1]) - 1

    def is_quadrilateral(self):
        if self.path_length != 4 or not self.is_closed or not self.is_continuous:
            return False

        for edge in self.list_of_edges:
            if edge.is_arc():
                return False

        return True

    def is_rectangular(self):
        if not self.is_quadrilateral():
            return False
        return (self.list_of_edges[0].is_perpendicular_to(self.list_of_edges[1]) and
                self.list_of_edges[1].is_perpendicular_to(self.list_of_edges[2]) and
                self.list_of_edges[2].is_perpendicular_to(self.list_of_edges[3]) and
                self.list_of_edges[3].is_perpendicular_to(self.list_of_edges[0]))

    def is_curved_top(self):
        if self.path_length != 5:
            return False

        for edge in self.list_of_edges:
            if not edge.is_arc() and not self.is_continuous:
                return False

        return True

    def convert_circle_to_points(self):
        if self.is_circle():
            circle_centre = Point2()
            circle_centre.x = self.list_of_edges[0].centre.x
            circle_centre.y = self.list_of_edges[0].centre.y
            circle_radius = self.list_of_edges[0].radius

            circle_list_of_points = [
                Point2(circle_centre.x - circle_radius, circle_centre.y),
                Point2(circle_centre.x, circle_centre.y + circle_radius),
                Point2(circle_centre.x + circle_radius, circle_centre.y),
                Point2(circle_centre.x, circle_centre.y - circle_radius)
            ]

            return circle_list_of_points

    def get_points_orientation(self, list_of_point_indices):
        # https://www.geeksforgeeks.org/convex-hull-set-1-jarviss-algorithm-or-wrapping/
        if is_list(list_of_point_indices):
            val = (((self.list_of_edges[list_of_point_indices[1]].minimum_y() - self.list_of_edges[
                list_of_point_indices[0]].minimum_y()) *
                    (self.list_of_edges[list_of_point_indices[2]].minimum_x() - self.list_of_edges[
                        list_of_point_indices[1]].minimum_x())) -
                   ((self.list_of_edges[list_of_point_indices[1]].minimum_x() - self.list_of_edges[
                       list_of_point_indices[0]].minimum_x()) *
                    (self.list_of_edges[list_of_point_indices[2]].minimum_y() - self.list_of_edges[
                        list_of_point_indices[1]].minimum_y())))

            if val == 0:
                return "Collinear"
            elif val > 0:
                return "Clockwise"
            else:
                return "Counterclockwise"
        raise TypeError("Input arguments must be objects of Point2")

    def get_leftmost_point_index(self):
        minimum_point_index = 0
        for index in range(1, self.path_length):
            if self.list_of_edges[index].p1.x < self.list_of_edges[minimum_point_index].p1.x:
                minimum_point_index = index
            elif self.list_of_edges[index].p1.x == self.list_of_edges[minimum_point_index].p1.x:
                if self.list_of_edges[index].p1.y > self.list_of_edges[minimum_point_index].p1.y:
                    minimum_point_index = index
        return minimum_point_index

    def get_convex_hull(self):
        convex_hull = Path2()
        if self.is_continuous:
            convex_hull = copy.deepcopy(self)
            if not self.is_closed:
                convex_hull.close_path()
            return convex_hull

        number_of_edges = self.path_length

        if number_of_edges < 3:
            raise IndexError("There must be at least three edges")

        leftmost_point_index = self.get_leftmost_point_index()

        first_point_index = leftmost_point_index

        while True:
            convex_hull.list_of_edges.append(self.list_of_edges[first_point_index])
            second_point_index = (first_point_index + 1) % number_of_edges

            for i in range(number_of_edges):
                if self.get_points_orientation([first_point_index, i, second_point_index]) == "Counterclockwise":
                    second_point_index = i

            first_point_index = second_point_index
            if first_point_index == leftmost_point_index:
                break
        convex_hull.close_path()
        return convex_hull

    def reverse(self):
        self.list_of_edges.reverse()
        for edge in self.list_of_edges:
            edge.reverse()

    def transform(self, transformation_matrix):
        for edge in self.list_of_edges:
            edge.transform(transformation_matrix)

    def generate_points(self):
        for count, edge in enumerate(self.list_of_edges):
            yield edge.p1
            if count + 1 == self.path_length:
                count = - 1
            next_edge = self.list_of_edges[count + 1]
            if edge.p2 == next_edge.p1:
                continue
            else:
                yield edge.p2

    def get_list_of_points(self):
        list_of_points = []
        for count, edge in enumerate(self.list_of_edges):
            list_of_points.append(edge.p1)
            if count + 1 == self.path_length:
                count = - 1
            next_edge = self.list_of_edges[count + 1]
            if edge.p2 == next_edge.p2:
                continue
            else:
                list_of_points.append(edge.p2)

        return list_of_points

    def get_oriented_bounding_box(self):
        class Box:
            def __init__(self):
                self.U = [Vector2(), Vector2()]
                self.index = [0, 0, 0, 0]
                self.U0_square_length = 0.0
                self.area = 0.0

        def smallest_box(first_point_index, last_point_index, list_of_points):
            box = Box()

            first_point = list_of_points[first_point_index]
            last_point = list_of_points[last_point_index]

            box.U[0] = last_point - first_point
            box.U[1] = box.U[0].get_perpendicular()
            box.U0_square_length = box.U[0].square_length()
            box.index = [last_point_index, last_point_index, last_point_index, last_point_index]

            origin = copy.deepcopy(last_point)
            support = []

            for index in range(4):
                support.append(Point2())

            index = 0
            for point in list_of_points:
                diff = point - origin
                v = Point2(box.U[0].dot(diff), box.U[1].dot(diff))

                if v.x > support[1].x or (v.x == support[1].x and v.y > support[1].y):
                    box.index[1] = index
                    support[1] = v

                if v.y > support[2].y or (v.y == support[2].y and v.x < support[2].x):
                    box.index[2] = index
                    support[2] = v

                if v.x < support[3].x or (v.x == support[3].x and v.y < support[3].y):
                    box.index[3] = index
                    support[3] = v

                index += 1

            scaled_width = support[1].x - support[3].x
            scaled_height = support[2].y
            box.area = (scaled_height * scaled_width) / box.U0_square_length

            return box

        def compute_angles(list_of_points, box, a, num_a):
            number_of_points = len(list_of_points)
            num_a = 0
            k0 = 3
            k1 = 0

            while k1 < 4:
                if box.index[k0] != box.index[k1]:
                    d = box.U[k0 & 1].invert() if k0 & 2 else box.U[k0 & 1]

                    j0 = box.index[k0]
                    j1 = j0 + 1

                    if j1 == number_of_points:
                        j1 = 0

                    e = list_of_points[j1] - list_of_points[j0]
                    dp = d.dot(e.get_perpendicular().invert())
                    e_square_length = e.square_length()
                    sin_theta_square = (dp * dp) / e_square_length
                    a[num_a] = (sin_theta_square, k0)
                    num_a += 1
                k0 = k1
                k1 += 1

            return num_a > 0, num_a

        def sort_angles(a, num_a):
            sort = [0, 1, 2, 3]
            if num_a > 1:
                if num_a == 2:
                    if a[sort[0]][0] > a[sort[1]][0]:
                        sort = [sort[1], sort[0], sort[2], sort[3]]
                elif num_a == 3:
                    if a[sort[0]][0] > a[sort[1]][0]:
                        sort = [sort[1], sort[0], sort[2], sort[3]]
                    if a[sort[0]][0] > a[sort[2]][0]:
                        sort = [sort[2], sort[1], sort[0], sort[3]]
                    if a[sort[1]][0] > a[sort[2]][0]:
                        sort = [sort[0], sort[2], sort[1], sort[3]]
                else:
                    if a[sort[0]][0] > a[sort[1]][0]:
                        sort = [sort[1], sort[0], sort[2], sort[3]]
                    if a[sort[2]][0] > a[sort[3]][0]:
                        sort = [sort[0], sort[1], sort[3], sort[2]]
                    if a[sort[0]][0] > a[sort[2]][0]:
                        sort = [sort[2], sort[1], sort[0], sort[3]]
                    if a[sort[1]][0] > a[sort[3]][0]:
                        sort = [sort[0], sort[3], sort[2], sort[1]]
                    if a[sort[1]][0] > a[sort[2]][0]:
                        sort = [sort[0], sort[2], sort[1], sort[3]]

            return sort

        def update_support(a, num_a, sort, list_of_points, visited, box):
            number_of_points = len(list_of_points)
            a_min = a[sort[0]]
            for k in range(num_a):
                a_var = a[sort[k]]
                if a_var[0] == a_min[0]:
                    box.index[a[1]] += 1
                    if box.index[a[1]] == number_of_points:
                        box.index[a[1]] = 0
                else:
                    break

            bottom = box.index[a_min[1]]
            if bottom in visited:
                return False, box
            visited.append(bottom)
            next_index = [0, 0, 0, 0]
            for k in range(4):
                next_index[k] = box.index[(a_min[1] + k) % 4]
            box.index = next_index

            j1 = box.index[0]
            j0 = j1 - 1
            if j0 < 0:
                j0 = number_of_points - 1

            box.U[0] = list_of_points[j1] - list_of_points[j0]
            box.U[1] = box.U[0].get_perpendicular()
            box.U0_square_length = box.U[0].square_length()

            diff = [list_of_points[box.index[1]] - list_of_points[box.index[3]],
                    list_of_points[box.index[2]] - list_of_points[box.index[0]]]
            box.area = (box.U[0].dot(diff[0]) * box.U[1].dot(diff[1])) / box.U0_square_length
            return True, box

        path_points = self.get_convex_hull().get_list_of_points()

        new_path_points = []
        number_of_new_path_points = len(new_path_points)
        for point in path_points:
            if number_of_new_path_points == 0:
                new_path_points.append(point)
                continue
            if point == new_path_points[-1]:
                continue
            new_path_points.append(point)

        path_points = new_path_points
        number_of_path_points = len(path_points)

        visited = []

        min_box = smallest_box(number_of_path_points - 1, 0, path_points)
        visited.append(min_box.index[0])

        box = copy.deepcopy(min_box)
        for i in range(number_of_path_points - 1):
            a = [None, None, None, None]
            num_a = 0
            res, num_a = compute_angles(path_points, box, a, num_a)
            if not res:
                break

            sort = sort_angles(a, num_a)
            res, box = update_support(a, num_a, sort, path_points, visited, box)
            if not res:
                break

            if box.area < min_box.area:
                min_box = copy.deepcopy(box)

        return min_box


def is_path2(input_variable):
    return isinstance(input_variable, Path2)
