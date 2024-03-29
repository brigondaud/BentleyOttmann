"""
segment between two points.
"""
from math import atan, pi
import struct
from geo.point import Point
from geo.quadrant import Quadrant
from geo.coordinates_hash import CoordinatesHash

class Segment:
    """
    oriented segment between two points.

    for example:

    - create a new segment between two points:

        segment = Segment([point1, point2])

    - create a new segment from coordinates:

        segment = Segment([Point([1.0, 2.0]), Point([3.0, 4.0])])

    - compute intersection point with other segment:

        intersection = segment1.intersection_with(segment2)

    """
    # Class attribute for the current point
    current_point = None

    # Adjuster usable with all segments (when computing key)
    adjuster = CoordinatesHash()

    def __init__(self, points, index=0):
        """
        create a segment from an array of two points.
        """
        self.endpoints = points
        self.index = index
    def __lt__(self, other):
        """
        compares two segments
        """
        key1 = self.compute_key(self.current_point)
        key2 = other.compute_key(other.current_point)
        return key1 < key2

    def compute_key(self, current_point):
        """
        computes the key for the bo algorithm
        """
        point1 = self.endpoints[0]
        point2 = self.endpoints[1]
        const = 0.0
        diff = point2.coordinates[0] - point1.coordinates[0]

        key_abs, key_ord = sweep_intersection(self, current_point)

        # Sign of the angle based on the position of the current point
        epsilon = 1
        if current_point.coordinates[0] > key_abs:
            epsilon = -1

        if current_point.coordinates[1] < key_ord:
            epsilon = -1

        if diff == 0:
            return (key_abs, epsilon*pi/2)
        if diff < 0:
            const = pi
        return (key_abs, epsilon*(const + \
            atan((point2.coordinates[1] - point1.coordinates[1])/(diff))))


    def copy(self):
        """
        return duplicate of given segment (no shared points with original,
        they are also copied).
        """
        return Segment([p.copy() for p in self.endpoints])

    def length(self):
        """
        return length of segment.
        example:
            segment = Segment([Point([1, 1]), Point([5, 1])])
            distance = segment.length() # distance is 4
        """
        return self.endpoints[0].distance_to(self.endpoints[1])

    def bounding_quadrant(self):
        """
        return min quadrant containing self.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.endpoints:
            quadrant.add_point(point)
        return quadrant

    def svg_content(self):
        """
        svg for tycat.
        """

        return '<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'.format(
            *self.endpoints[0].coordinates,
            *self.endpoints[1].coordinates)

    def intersection_with(self, other):
        """
        intersect two 2d segments.
        only return point if included on the two segments.
        """
        i = self.line_intersection_with(other)
        if i is None:
            return  # parallel lines

        if self.contains(i) and other.contains(i):
            return i

    def line_intersection_with(self, other):
        """
        return point intersecting with the two lines passing through
        the segments.
        none if lines are almost parallel.
        """
        # solve following system :
        # intersection = start of self + alpha * direction of self
        # intersection = start of other + beta * direction of other
        directions = [s.endpoints[1] - s.endpoints[0] for s in (self, other)]
        denominator = directions[0].cross_product(directions[1])
        if abs(denominator) < 0.000001:
            # almost parallel lines
            return
        start_diff = other.endpoints[0] - self.endpoints[0]
        alpha = start_diff.cross_product(directions[1]) / denominator
        return self.endpoints[0] + directions[0] * alpha

    def contains(self, possible_point):
        """
        is given point inside us ?
        be careful, determining if a point is inside a segment is a difficult problem
        (it is in fact a meaningless question in most cases).
        you might get wrong results for points extremely near endpoints.
        """
        distance = sum(possible_point.distance_to(p) for p in self.endpoints)
        return abs(distance - self.length()) < 0.000001

    def __str__(self):
        return "Segment([" + str(self.endpoints[0]) + ", " + \
            str(self.endpoints[1]) + "])"

    def __repr__(self):
        return "Segment[" + repr(self.endpoints[0]) + ", " + \
            repr(self.endpoints[1]) + "]"

def sweep_intersection(segment, current_point):
    """
    computes and returns the abscissa of the intersection beetween the
    sweeping line and the segment.
    """
    # Creates a segment that corresponds to the sweeping line around segment
    sweep = Segment([Point([0, current_point.coordinates[1]]),
                     Point([1, current_point.coordinates[1]])])
    key_point = segment.line_intersection_with(sweep)


    # The key_point is None if segment is horizontal
    if key_point is not None:
        key_point = Segment.adjuster.hash_point(key_point)
        return key_point.coordinates
    else:
        return current_point.coordinates

def load_segments(filename):
    """
    loads given .bo file.
    returns a vector of segments.
    """
    coordinates_struct = struct.Struct('4d')
    segments = []
    adjuster = CoordinatesHash()

    with open(filename, "rb") as bo_file:
        packed_segment = bo_file.read(32)
        while packed_segment:
            coordinates = coordinates_struct.unpack(packed_segment)
            raw_points = [Point(coordinates[0:2]), Point(coordinates[2:])]
            adjusted_points = [adjuster.hash_point(p) for p in raw_points]
            segments.append(Segment(adjusted_points))
            packed_segment = bo_file.read(32)

    return adjuster, segments
