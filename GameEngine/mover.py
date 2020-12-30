import pygame


class Mover():
    """Base class for game objects that move."""

    def move(self, delta, pos, heading):
        pass


class MoverVelocity():

    def __init__(self, velocity_decay_factor):
        self.velocity = 0.0
        self.velocity_decay_factor = velocity_decay_factor

    def move(self, delta, pos, heading):
        """Computes movement from the given parameters."""
        delta_pos = pygame.math.Vector2()
        delta_pos.from_polar((delta / -1000.0 * self.velocity, 90.0 - heading))
        self.velocity = self.velocity * self.velocity_decay_factor
        return (pos + delta_pos, heading)

    def set_velocity(self, velocity):
        self.velocity = velocity
