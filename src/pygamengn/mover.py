import numpy
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase
from pygamengn.interpolator import *


class Mover(GameObjectBase):
    """Base class for game objects that move."""

    def move(self, delta, pos, heading):
        pass


@ClassRegistrar.register("MoverVelocity")
class MoverVelocity(Mover):
    """Velocity-based mover."""

    def __init__(self, velocity_decay_factor, velocity, max_velocity, angular_velocity):
        self.velocity = velocity
        self.velocity_decay_factor = velocity_decay_factor
        self.max_velocity = max_velocity
        self.angular_velocity = angular_velocity

    def move(self, delta, pos, heading):
        """Computes movement from the given parameters."""
        theta = numpy.deg2rad(90 - heading)
        direction = pygame.Vector2(numpy.cos(theta), numpy.sin(theta))
        delta_pos = direction * delta / -1000.0 * self.velocity
        self.velocity = self.velocity * self.velocity_decay_factor
        return (pos + delta_pos, heading)

    def set_velocity(self, velocity):
        self.velocity = velocity


@ClassRegistrar.register("MoverVelDir")
class MoverVelDir(Mover):
    """Velocity- and direction-based mover."""

    def __init__(self, velocity, direction):
        self.velocity = velocity
        self.direction = direction

    def move(self, delta, *_):
        return self.direction * delta / 1000.0 * self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_direction(self, direction: pygame.Vector2):
        """Sets direction of movement. direction is a pygame.Vector2."""
        self.direction = direction


@ClassRegistrar.register("MoverTime")
class MoverTime(Mover):
    """Time-based mover."""

    def __init__(
        self,
        duration = 0,
        origin = pygame.Vector2(0, 0),
        destination = pygame.Vector2(1, 0),
        interpolationMode = InterpolationMode.LINEAR
    ):
        self.__duration = duration
        self.__origin = origin
        self.__destination = destination
        self.__elapsed_time = 0
        self.__interpolator = Interpolator(duration, origin, destination, interpolationMode)

    def move(self, delta, *_):
        self.__elapsed_time += delta
        return self.__interpolator.get(self.__elapsed_time)

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, d):
        self.__duration = d
        self.__interpolator.duration = d

    def is_arrived(self) -> bool:
        return self.__elapsed_time >= self.__duration
