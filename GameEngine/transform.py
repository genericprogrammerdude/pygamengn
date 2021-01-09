import numpy
import pygame


class Transform():
    """Class to manage 2d affine transformations."""

    def __init__(self, translation=(0.0, 0.0), theta=0.0, scale=1.0):
        t = self.translation_matrix(translation)
        r = self.rotation_matrix(-theta)
        s = self.scale_matrix(scale)
        self.matrix = numpy.dot(numpy.dot(t, r), s)

    def apply(self, point):
        """Applies the transform to the given point."""
        m = numpy.dot(self.matrix, numpy.array([point[0], point[1], 1.0]).transpose())
        return pygame.Vector2(m[0], m[1])

    @classmethod
    def translation_matrix(cls, translation=(0.0, 0.0)):
        m = numpy.identity(3)
        m[0][2] = translation[0]
        m[1][2] = translation[1]
        return m

    @classmethod
    def rotation_matrix(cls, theta):
        rad = numpy.deg2rad(theta)
        cos = numpy.cos(rad)
        sin = numpy.sin(rad)

        m = numpy.identity(3)
        m[0][0] = cos
        m[0][1] = -sin
        m[1][0] = sin
        m[1][1] = cos

        return m

    @classmethod
    def scale_matrix(cls, scale):
        m = numpy.identity(3)
        m[0][0] = scale
        m[1][1] = scale

        return m

    @classmethod
    def rotate(cls, point, theta):
        m = numpy.dot(cls.rotation_matrix(theta), numpy.array([point[0], point[1], 1.0]).transpose())
        return pygame.Vector2(m[0], m[1])
