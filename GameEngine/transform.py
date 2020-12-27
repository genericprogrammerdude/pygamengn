import numpy


class Transform():
    """Class to manage 2d affine transformations."""

    def __init__(self, translation=(0.0, 0.0), theta=0.0, scale=1.0):
        rad = numpy.deg2rad(theta)
        cos = numpy.cos(rad)
        sin = numpy.sin(rad)
        self.matrix = numpy.array([
            [scale * cos, -scale * sin, translation[0] * scale * cos - translation[1] * scale * sin],
            [scale * sin, scale * cos, translation[0] * scale * sin + translation[1] * scale * cos],
            [  0.0, 0.0, 1.0]
        ])

        t = self.translation_matrix(translation)
        r = self.rotation_matrix(theta)
        s = self.scale_matrix(scale)

        print("--------")
        print(numpy.dot(r, numpy.dot(s, t)))
        print()
        print(self.matrix)
        print("--------")

    def apply(self, point):
        """Applies the transform to the given point."""
        m = numpy.dot(self.matrix, numpy.array([[point[0]], [point[1]], [1.0]]))
        return (m[0][0], m[1][0])

    def translation_matrix(self, translation=(0.0, 0.0)):
        m = numpy.identity(3)
        m[0][2] = translation[0]
        m[1][2] = translation[1]
        return m

    def rotation_matrix(self, theta):
        rad = numpy.deg2rad(theta)
        cos = numpy.cos(rad)
        sin = numpy.sin(rad)

        m = numpy.identity(3)
        m[0][0] = cos
        m[0][1] = -sin
        m[1][0] = sin
        m[1][1] = cos

        return m

    def scale_matrix(self, scale):
        m = numpy.identity(3)
        m[0][0] = scale
        m[1][1] = scale

        return m
