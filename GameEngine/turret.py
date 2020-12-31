import math
import random

from game_object import GameObject
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Turret")
class Turret(GameObject):
    """Turret that will fire at the given target."""

    def __init__(self, image, projectile_type, enemies, fire_freq, **kwargs):
        super().__init__(image, **kwargs)
        self.projectile_type = projectile_type
        self.target = None
        self.fire_freq = fire_freq
        self.time_since_last_fire = random.randint(0, fire_freq)
        self.enemies = enemies

    def set_target(self, target):
        """Sets the target to attack."""
        self.target = target

    def update(self, delta):
        super().update(delta)

        if self.target:
            if self.target.alive():
                fire_dir = self.target.pos - self.pos
                heading = math.degrees(math.atan2(fire_dir[0], fire_dir[1]) - math.pi)
                self.set_heading(heading)

                self.time_since_last_fire = self.time_since_last_fire + delta
                if self.time_since_last_fire >= self.fire_freq and self.alive():
                    self.fire()
            else:
                self.time_since_last_fire = self.fire_freq
                self.target = None

    def fire(self):
        """Fires a projectile_type object at the target."""
        projectile = GameObjectFactory.create(self.projectile_type, enemies=self.enemies)
        projectile.set_pos(self.pos)
        projectile.set_heading(self.heading)
        projectile.transform()

        group = self.groups()[0]
        group.add(projectile)
        group.move_to_back(projectile)

        self.time_since_last_fire = 0
