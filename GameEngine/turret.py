from game_object import GameObject
from ship import Ship


class Turret(GameObject):
    """Turret that will fire at the given target."""

    def __init__(self, base_image_fname, laser_image_fname):
        super().__init__(base_image_fname)
        self.laser_image_fname = laser_image_fname
        self.target = None
        self.fire_freq = 500
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
        """Fires a shot at the target."""

        fire_dir = self.pos - self.target.pos
        fire_dir.normalize()
        angle, _ = fire_dir.as_polar()
        shot = Ship(self.laser_image_fname)
        shot.set_pos(self.pos)
        shot.set_angle(angle)
        shot.set_velocity(1000)
        self.groups()[0].add(shot)

        self.time_since_last_fire = 0
