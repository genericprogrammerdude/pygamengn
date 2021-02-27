import math

from class_registrar import ClassRegistrar
from game_object import GameObject


@ClassRegistrar.register("Turret")
class Turret(GameObject):
    """Turret that will fire at the given target."""

    def __init__(self, projectile_type, fire_freq, health, score_on_die, shot_sound, **kwargs):
        super().__init__(**kwargs)
        self.projectile_type = projectile_type
        self.target = None
        self.fire_freq = fire_freq
        self.time_since_last_fire = 0
        self.health = health
        self.score_on_die = score_on_die
        self.shot_sound = shot_sound

    def set_target(self, target):
        """Sets the target to attack."""
        self.target = target

    def update(self, delta):
        super().update(delta)

        if self.target:
            if self.target.alive():
                fire_dir = self.target.position - self.position
                heading = math.degrees(math.atan2(fire_dir[0], fire_dir[1]) - math.pi)
                self.set_heading(heading)

                # Increase fire frequency as the turret gets closer to its target
                distance = fire_dir.length()
                delta_factor = 1.0
                if distance < 1000:
                    delta_factor = 4.0 - distance / 250.0
                self.time_since_last_fire = self.time_since_last_fire + delta * delta_factor
                if self.time_since_last_fire >= self.fire_freq and self.alive():
                    self.fire()
            else:
                self.time_since_last_fire = self.fire_freq
                self.target = None

    def fire(self):
        """Fires a projectile_type object at the target."""
        projectile = self.projectile_type.create()
        projectile.position = self.position
        projectile.set_heading(self.heading)
        projectile.transform()
        if self.parent:
            # Set projectile parent the same as the turret's to avoid collisions between projectiles and turret parents
            projectile.set_parent(self.parent)
        self.time_since_last_fire = 0
        self.shot_sound.play()

    def die(self, instigator):
        """Die."""
        try:
            instigator.add_score(self.score_on_die)
        except AttributeError:
            pass
        super().die(instigator)
