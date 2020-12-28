import math

from game_object import GameObject
from projectile import Projectile


class Turret(GameObject):
    """Turret that will fire at the given target."""

    def __init__(self, turret_image, projectile_image, enemies):
        super().__init__(turret_image)
        self.projectile_image = projectile_image
        self.target = None
        self.fire_freq = 1000
        self.time_since_last_fire = 0
        self.enemies = enemies

    def set_target(self, target):
        """Sets the target to attack."""
        self.target = target

    def update(self, delta):
        super().update(delta)

        fire_dir = self.target.pos - self.pos
        heading = math.degrees(math.atan2(fire_dir[0], fire_dir[1]) - math.pi)
        self.set_heading(heading)

        self.time_since_last_fire = self.time_since_last_fire + delta
        if self.time_since_last_fire >= self.fire_freq and self.target != None:
            self.fire()

    def fire(self):
        """Fires a Projectile at the target."""
        projectile = Projectile(self.projectile_image, enemies=self.enemies)
        projectile.set_pos(self.pos)
        projectile.set_heading(self.heading)
        projectile.transform()
        projectile.set_velocity(500)

        group = self.groups()[0]
        group.add(projectile)
        group.move_to_back(projectile)

        self.time_since_last_fire = 0
