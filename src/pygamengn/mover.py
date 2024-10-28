import numpy
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase


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
class MoverTime(MoverVelDir):
    """Time-based mover."""

    def __init__(self, eta: float, origin = pygame.Vector2(0, 0), destination = pygame.Vector2(1, 0)):
        self.eta = eta / 1000.0
        diff = pygame.Vector2(destination) - pygame.Vector2(origin)
        super().__init__(diff.length() / self.eta, diff.normalize())

    def set_ori_dest(self, origin: pygame.Vector2, destination: pygame.Vector2):
        diff = destination - origin
        self.set_velocity(diff.length() / self.eta)
        self.set_direction(diff.normalize())
