from game_object import GameObject
from projectile import Projectile


class Turret(GameObject):
    """Turret that will fire at the given target."""

    def __init__(self, base_image_fname, laser_image_fname):
        super().__init__(base_image_fname)
        self.laser_image_fname = laser_image_fname
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
        _, angle = fire_dir.as_polar()

        projectile = Projectile(self.laser_image_fname)
        projectile.set_pos(self.pos)
        projectile.set_angle(270 - angle)
        projectile.transform()
        projectile.set_velocity(500)

        group = self.groups()[0]
        group.add(projectile)
        group.move_to_back(projectile)

        self.time_since_last_fire = 0
