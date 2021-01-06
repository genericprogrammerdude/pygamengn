import unittest

import numpy

import geometry


class TestGeometry(unittest.TestCase):

    def test_segment_line_parallel(self):
        # Parallel segments
        a = geometry.Segment((0, 0), (4, 2))
        b = geometry.Segment((1, 0), (3, 1))
        self.assertEqual(a.intersect(b), None)

    def test_segment_line_21(self):
        # Intersecting at (2, 1)
        a = geometry.Segment((0, 0), (4, 2))
        b = geometry.Segment((0, 3), (3, 0))
        self.assertEqual(a.intersect(b).all(), numpy.array([2, 1]).all())

    def test_segment_line_105(self):
        # Intersecting at (1, 0.5)
        a = geometry.Segment((0, 0), (4, 2))
        b = geometry.Segment((2, 0), (0, 1))
        self.assertEqual(a.intersect(b).all(), numpy.array([1, 0.5]).all())

    def test_line_line(self):
        # No segment intersect, but lines do
        a = geometry.Segment((2, 1), (4, 2))
        b = geometry.Segment((0, 1), (2, 0))
        self.assertEqual(a.intersect(b), None)

    def test_line_line_no_segment(self):
        # No segment intersect, but lines do
        a = geometry.Segment((2, 1), (4, 2))
        b = geometry.Segment((0, 1), (2, 0))
        self.assertEqual(geometry.line_intersect(a.p0, a.p1, b.p0, b.p1).all(), numpy.array([1, 0.5]).all())

    def test_ray(self):
        ray = geometry.Ray((1, 2), 45)
        print(ray)
#         print(ray.point_in_ray((2, 3)))
#         print(ray.point_in_ray((0, 1)))

    if __name__ == "__main__":
        unittest.main()
