import numpy


class Segment:

    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

    def intersect(self, segment):
        ip = line_intersect(self.p0, self.p1, segment.p0, segment.p1)
        if ip is not None:
            if not (self.point_in_segment(ip) and segment.point_in_segment(ip)):
                return None
        return ip

    def point_in_segment(self, point):
        if self.p0[0] != self.p1[0]:
            # self is not vertical
            return((self.p0[0] >= point[0] and self.p1[0] <= point[0]) or
                   (self.p0[0] <= point[0] and self.p1[0] >= point[0]))
        else:
            # self is vertical -> test y coordinate
            return((self.p0[1] >= point[1] and self.p1[1] <= point[1]) or
                   (self.p0[1] <= point[1] and self.p1[1] >= point[1]))


class Ray:

    def __init__(self, origin, angle):
        self.origin = origin
        self.angle = angle

    def inersect_segment(self, segment):
        p0 = self.origin
        theta = numpy.deg2rad(self.angle)
        p1 = (p0[0] + numpy.cos(theta), p0[1] + numpy.sin(theta))
        ip = line_intersect(p0, p1, segment.p0, segment.p1)
        if segment.point_in_segment(ip) and self.point_in_ray(ip):
            return ip
        return None

    def point_in_ray(self, point):
        theta = numpy.deg2rad(self.angle)
        cos = numpy.cos(theta)
        sin = numpy.sin(theta)
        p0 = numpy.array(self.origin)
        p1 = numpy.array(point)
        diff = p1 - p0
        print(diff[0] / cos, diff[1] / sin)


def line_intersect(a1, a2, b1, b2):
    """
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line

    Lifted off https://stackoverflow.com/questions/3252194/numpy-and-line-intersections
    """
    s = numpy.vstack([a1, a2, b1, b2])  # s for stacked
    h = numpy.hstack((s, numpy.ones((4, 1))))  # h for homogeneous
    l1 = numpy.cross(h[0], h[1])  # get first line
    l2 = numpy.cross(h[2], h[3])  # get second line
    x, y, z = numpy.cross(l1, l2)  # point of intersection
    if z == 0:  # lines are parallel
        return None  # (float('inf'), float('inf'))
    return numpy.array([x / z, y / z])


def test_segment_line():
    # Parallel segments
    a = Segment((0, 0), (4, 2))
    b = Segment((1, 0), (3, 1))
    print(a.intersect(b))

    # Intersecting at (2, 1)
    a = Segment((0, 0), (4, 2))
    b = Segment((0, 3), (3, 0))
    print(a.intersect(b))

    # Intersecting at (1, 0.5)
    a = Segment((0, 0), (4, 2))
    b = Segment((2, 0), (0, 1))
    print(a.intersect(b))

    # No segment intersect, but lines do
    a = Segment((2, 1), (4, 2))
    b = Segment((0, 1), (2, 0))
    print(a.intersect(b))
    print(line_intersect((2, 1), (4, 2), (0, 1), (2, 0)))


if __name__ == "__main__":
    ray = Ray((1, 2), 45)
    print(ray.point_in_ray((2, 3)))
    print(ray.point_in_ray((0, 1)))
