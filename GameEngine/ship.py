import pygame

from animated_texture import AnimatedTexture
from game_object import GameObject


class Ship(GameObject):
    """Space ship game object."""

    def __init__(self, image_fname, velocity_decay_factor=1.0):
        super().__init__(image_fname)
        self.velocity = 0.0
        self.velocity_decay_factor = velocity_decay_factor
        self.explosion = AnimatedTexture("Assets/Explosions/explosion1.png", (256, 256), 2000)

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
        if not self.explosion.is_playing:
            group = self.groups()[0]
            group.add(self.explosion)
            group.move_to_front(self.explosion)
            self.explosion.set_pos(self.pos - local_pos)
            self.explosion.play()
