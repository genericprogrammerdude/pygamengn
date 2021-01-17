from asteroid import Asteroid
from game_object import GameObject
from game_object_factory import GameObjectFactory
from health_bar import HealthBar
from mover import MoverVelocity
from nav_arrow import NavArrow
from projectile import Projectile


@GameObjectFactory.register("Ship")
class Ship(GameObject):
    """Space ship game object."""

    def __init__(self, projectile_type, fire_freq, mover, death_effect, damage, nav_arrow, **kwargs):
        super().__init__(**kwargs)
        self.mover = mover
        self.projectile_type = projectile_type
        self.fire_freq = fire_freq
        self.time_since_last_fire = self.fire_freq
        self.death_effect = death_effect
        self.damage = damage
        self.nav_arrow = nav_arrow
        self.score = 0
        self.death_callbacks = []

    def update(self, delta):
        """Updates the ship."""
        # Translate according to velocity
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        # Now do the regular GameObject update
        super().update(delta)
        self.time_since_last_fire += delta

        if self.waypoint:
            # Position and orient the nav arrow
            direction = (self.waypoint.pos - self.pos).normalize()
            self.nav_arrow.set_pos(self.pos + direction * 150)
            _, angle = direction.as_polar()
            self.nav_arrow.set_heading(270 - angle)

    def set_velocity(self, velocity):
        """Sets the ship's velocity."""
        self.mover.set_velocity(velocity)

    def fire(self):
        """Fires a Projectile at the target."""
        if self.time_since_last_fire > self.fire_freq and self.alive():
            projectile = GameObjectFactory.create(self.projectile_type)
            projectile.set_pos(self.pos)
            projectile.set_heading(self.heading)
            projectile.transform()
            projectile.set_parent(self)
            self.time_since_last_fire = 0

    def add_score(self, score):
        self.score += score

    def die_callback(self, callback):
        """Adds a callback to invoke when this game object dies."""
        self.death_callbacks.append(callback)

    def death_effect_callback(self):
        """Callback for when the death effect is done playing."""
        for callback in self.death_callbacks:
            callback()

    def set_waypoint(self, waypoint):
        """Sets the waypoint the ship should go to."""
        self.waypoint = waypoint
        self.nav_arrow.set_target(waypoint)

    def die(self, instigator):
        super().die(instigator)
        self.nav_arrow.die(instigator)
