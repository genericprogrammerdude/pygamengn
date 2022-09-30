import random

import numpy
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject
from pygamengn.health_bar import HealthBar
from pygamengn.mover import MoverVelocity
from pygamengn.projectile import Projectile

from pygamengn.network.replicated_property import ReplicatedProperty

from asteroid import Asteroid
from nav_arrow import NavArrow
from waypoint import Waypoint


@ClassRegistrar.register("Ship")
class Ship(GameObject):
    """Space ship game object."""

    def __init__(self, projectile_type, fire_freq, mover, waypoint, shot_sound, **kwargs):
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
        self.shot_sound = shot_sound
        self.waypoint.set_enter_callback(self.place_waypoint)
        self.waypoint.visible = False

    def get_replicated_props(self):
        """Returns a list of properties that this object will replicate from server to connected clients."""
        return super().get_replicated_props() + [
            ReplicatedProperty("velocity")
        ]

    def update(self, delta):
        """Updates the ship."""
        # Translate according to velocity
        self.position, self.heading = self.mover.move(delta, self.position, self.heading)
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

    @property
    def velocity(self):
        return self.mover.velocity

    @velocity.setter
    def velocity(self, velocity):
        """Sets the ship's velocity."""
        self.mover.set_velocity(velocity)

    def fire(self):
        """Fires a Projectile at the target."""
        if self.time_since_last_fire > self.fire_freq and self.alive():
            projectile = self.projectile_type.create()
            projectile.position = self.position
            projectile.heading = self.heading
            projectile.transform()
            projectile.set_parent(self)
            self.time_since_last_fire = 0
            self.shot_sound.play()

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
        pos = self.position + self.waypoint.distance * pygame.Vector2(numpy.cos(angle), numpy.sin(angle))
        self.waypoint.position = pos
        if gob:
            # The presence of a valid gob indicates we're here as a result of a collision
            self.waypoints += 1
        self.waypoint.set_number(self.waypoints + 1)
