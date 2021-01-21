import random

import numpy
import pygame

from asteroid import Asteroid
from game_object import GameObject
from game_object_factory import GameObjectFactory
from health_bar import HealthBar
from mover import MoverVelocity
from nav_arrow import NavArrow
from projectile import Projectile
from waypoint import Waypoint


@GameObjectFactory.register("Ship")
class Ship(GameObject):
    """Space ship game object."""

    def __init__(self, projectile_type, fire_freq, mover, waypoint, **kwargs):
        super().__init__(**kwargs)
        self.mover = mover
        self.projectile_type = projectile_type
        self.fire_freq = fire_freq
        self.time_since_last_fire = self.fire_freq
        self.score = 0
        self.kills = 0
        self.waypoints = 0
        self.death_callbacks = []
        self.waypoint = waypoint
        self.waypoint.set_enter_callback(self.place_waypoint)
        self.waypoint.visible = False

    def update(self, delta):
        """Updates the ship."""
        # Translate according to velocity
        self.pos, self.heading = self.mover.move(delta, self.pos, self.heading)
        # Now do the regular GameObject update
        super().update(delta)
        self.time_since_last_fire += delta
        if not self.waypoint.visible:
            self.waypoint.visible = True
            self.place_waypoint()

    def attach(self, game_object, offset, take_parent_transform):
        """Attaches a game object to this game object at the give offset."""
        super().attach(game_object, offset, take_parent_transform)
        try:
            # Set the waypoint to point to -- only applies to NavArrow attachment
            game_object.set_waypoint(self.waypoint)
        except AttributeError:
            pass

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

    def die_callback(self, callback):
        """Adds a callback to invoke when this game object dies."""
        self.death_callbacks.append(callback)

    def death_effect_callback(self):
        """Callback for when the death effect is done playing."""
        self.waypoint.die(None)
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

    def place_waypoint(self, gob=None):
        angle = numpy.deg2rad(random.randrange(0, 360))
        pos = self.pos + self.waypoint.distance * pygame.Vector2(numpy.cos(angle), numpy.sin(angle))
        self.waypoint.set_pos(pos)
        if gob:
            # The presence of a valid gob indicates we're here as a result of a collision
            self.waypoints += 1
        self.waypoint.set_number(self.waypoints + 1)
