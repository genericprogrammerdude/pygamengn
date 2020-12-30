from game_object import GameObject
from game_object_factory import GameObjectFactory
from mover import MoverVelocity
from projectile import Projectile


@GameObjectFactory.register("Ship")
class Ship(GameObject):
    """Space ship game object."""

    def __init__(self, image, velocity_decay_factor):
        super().__init__(image)
        self.mover = MoverVelocity(velocity_decay_factor)

    def update(self, delta):
        """Updates the ship."""
        # Translate according to velocity
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        # Now do the regular GameObject update
        super().update(delta)

    def set_velocity(self, velocity):
        """Sets the ship's velocity."""
        self.mover.set_velocity(velocity)

    def fire(self):
        """Fires a Projectile at the target."""
        projectile = Projectile(self.projectile_image, enemies=self.enemies, explosion_atlas=self.explosion_atlas)
        projectile.set_pos(self.pos)
        projectile.set_heading(self.heading)
        projectile.transform()
        projectile.set_velocity(500)

        group = self.groups()[0]
        group.add(projectile)
        group.move_to_back(projectile)

        self.time_since_last_fire = 0
