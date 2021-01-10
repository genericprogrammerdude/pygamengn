import math

from game_object import GameObject
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Turret")
class Turret(GameObject):
    """Turret that will fire at the given target."""

    def __init__(self, image, projectile_type, fire_freq, health, death_effect, score_on_die, **kwargs):
        super().__init__(image, **kwargs)
        self.projectile_type = projectile_type
        self.target = None
        self.fire_freq = fire_freq
        self.time_since_last_fire = 0
        self.health = health
        self.death_effect = death_effect
        self.score_on_die = score_on_die

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
        projectile = GameObjectFactory.create(self.projectile_type)
        projectile.set_pos(self.pos)
        projectile.set_heading(self.heading)
        projectile.transform()
        if self.parent:
            # Set projectile parent the same as the turret's to avoid collisions between projectiles and turret parents
            projectile.set_parent(self.parent)
        self.time_since_last_fire = 0

    def die(self, instigator):
        """Die."""
        try:
            instigator.add_score(self.score_on_die)
        except AttributeError:
            pass
        super().die(instigator)
