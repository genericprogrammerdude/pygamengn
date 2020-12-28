import pygame

from animated_texture import AnimatedTexture
from atlas import Atlas
from game_object import GameObject


class Ship(GameObject):
    """Space ship game object."""

    def __init__(self, image, explosion_atlas=None, velocity_decay_factor=1.0):
        super().__init__(image)
        self.velocity = 0.0
        self.velocity_decay_factor = velocity_decay_factor
        self.explosion_atlas = explosion_atlas

    def update(self, delta):
        """Updates the ship."""

        # Translate according to velocity
        delta_pos = pygame.math.Vector2()
        delta_pos.from_polar((delta / -1000.0 * self.velocity, 90.0 - self.heading))
        self.set_pos(self.pos + delta_pos)
        self.velocity = self.velocity * self.velocity_decay_factor

        # Now do the regular GameObject update
        super().update(delta)

    def set_velocity(self, velocity):
        """Sets the ship's velocity in screen units per second."""
        self.velocity = velocity

    def collide(self, collider, local_pos):
        explosion = AnimatedTexture(self.explosion_atlas, 750)
        group = self.groups()[0]
        group.add(explosion)
        group.move_to_front(explosion)
        explosion.set_pos(collider.pos)
        explosion.play()
