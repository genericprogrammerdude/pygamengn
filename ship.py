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

    def __init__(self, projectile_type, fire_freq, mover, death_effect, damage, **kwargs):
        super().__init__(**kwargs)
        self.mover = mover
        self.projectile_type = projectile_type
        self.fire_freq = fire_freq
        self.time_since_last_fire = self.fire_freq
        self.death_effect = death_effect
        self.damage = damage
        self.score = 0
        self.kills = 0
        self.waypoints = 0
        self.death_callbacks = []

    def update(self, delta):
        """Updates the ship."""
        # Translate according to velocity
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        # Now do the regular GameObject update
        super().update(delta)
        self.time_since_last_fire += delta

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
        self.kills += 1
        self.score += score

    def increment_waypoint_count(self):
        self.waypoints += 1
        self.waypoint.set_number(self.waypoints + 1)

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
        for attachment in self.attachments:
            try:
                attachment.game_object.set_waypoint(waypoint)
            except AttributeError:
                pass
