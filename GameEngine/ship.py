from game_object import GameObject
from mover import MoverVelocity


class Ship(GameObject):
    """Space ship game object."""

    def __init__(self, image, velocity_decay_factor=1.0):
        super().__init__(image)
        self.mover = MoverVelocity(velocity_decay_factor)

    def update(self, delta):
        """Updates the ship."""
        # Translate according to velocity
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        # Now do the regular GameObject update
        super().update(delta)

    def set_velocity(self, velocity):
        """Sets the ship's velocity in screen units per second."""
        self.mover.set_velocity(velocity)
