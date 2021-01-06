import numpy


class Segment:

    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1

    def __str__(self):
        return "Segment(({0}, {1}), ({2}, {3}))".format(
            self.p0[0],
            self.p0[1],
            self.p1[0],
            self.p1[1]
        )

    def intersect_segment(self, segment):
        ip = line_intersect(self.p0, self.p1, segment.p0, segment.p1)
        if ip is not None:
            if not (self.point_in_segment(ip) and segment.point_in_segment(ip)):
                return None
        return ip

    def intersect_line(self, segment):
        """Same as intersect_segment(), but doesn't check for intersection point in segment."""
        ip = line_intersect(self.p0, self.p1, segment.p0, segment.p1)
        if ip is not None:
            if not self.point_in_segment(ip):
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

    def __init__(self, origin, angle_deg):
        self.origin = origin
        self.angle_deg = angle_deg

    def __str__(self):
        return "Ray(({0}, {1}), {2})".format(
            self.origin[0],
            self.origin[1],
            self.angle_deg
        )

    def inersect_segment(self, segment):
        p0 = self.origin
        theta = numpy.deg2rad(self.angle_deg)
        cos = numpy.cos(theta)
        sin = numpy.sin(theta)
        p1 = (p0[0] + cos, p0[1] + sin)
        ip = line_intersect(p0, p1, segment.p0, segment.p1)
        if ip is not None and segment.point_in_segment(ip) and self.point_in_ray(ip):
            return ip
        return None

    def get_segment(self):
        p0 = self.origin
        theta = numpy.deg2rad(self.angle_deg)
        cos = numpy.cos(theta)
        sin = numpy.sin(theta)
        p1 = (p0[0] + cos, p0[1] + sin)
        return Segment(p0, p1)

    def point_in_ray(self, point):
        """DO NOT USE THIS. IT DOESN'T WORK."""
        return None
        theta = numpy.deg2rad(self.angle_deg)
        cos = numpy.cos(theta)
        sin = numpy.sin(theta)
        factor_x = factor_y = 0
        if cos != 0:
            factor_x = ((point[0] - self.origin[0]) / cos)
            return (factor_x < 0)
        if sin != 0:
            factor_y = ((point[1] - self.origin[1]) / sin)
            return (factor_y < 0)
        return False


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


def get_quadrant(angle_deg):
    """Returns the quadrant for the given angle. Angle must be in degrees and normalized to [0, 360)."""
    quadrant = 1

    if angle_deg >= 90 and angle_deg < 180:
        quadrant = 2
    elif angle_deg >= 180 and angle_deg < 270:
        quadrant = 3
    elif angle_deg >= 270 and angle_deg < 360:
        quadrant = 4

    return quadrant
