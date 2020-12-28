from game_object import GameObject
from projectile import Projectile


class Turret(GameObject):
    """Turret that will fire at the given target."""

    def __init__(self, turret_image, projectile_image):
        super().__init__(turret_image)
        self.projectile_image = projectile_image
        self.target = None
        self.fire_freq = 1000
        self.time_since_last_fire = 0

    def set_target(self, target):
        """Sets the target to attack."""
        self.target = target

    def update(self, delta):
        super().update(delta)

        self.time_since_last_fire = self.time_since_last_fire + delta
        if self.time_since_last_fire >= self.fire_freq and self.target != None:
            self.fire()

    def fire(self):
        """Fires a Projectile at the target."""
        fire_dir = self.target.pos - self.pos
        _, heading = fire_dir.as_polar()

        projectile = Projectile(self.projectile_image)
        projectile.set_pos(self.pos)
        projectile.set_heading(270 - heading)
        projectile.transform()
        projectile.set_velocity(500)

        group = self.groups()[0]
        group.add(projectile)
        group.move_to_back(projectile)

        self.time_since_last_fire = 0
