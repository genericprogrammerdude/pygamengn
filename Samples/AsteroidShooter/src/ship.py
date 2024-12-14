import random

import numpy
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.console_registrar import ConsoleRegistrar
from pygamengn.game_object import GameObject

from asteroid import Asteroid
from nav_arrow import NavArrow, PowerupArrow
from shield import Shield
from shield_powerup import ShieldPowerup
from waypoint import Waypoint


@ClassRegistrar.register("Ship")
class Ship(GameObject):
    """Space ship game object."""

    __god_mode = False

    @classmethod
    def toggle_god_mode(cls):
        Ship.__god_mode = not Ship.__god_mode
        return f"god mode {"enabled" if Ship.__god_mode else "disabled"}"

    @classmethod
    def god_mode(cls) -> bool:
        return cls.__god_mode


    def __init__(self, projectile_type, fire_freq, mover, shot_sound, waypoint, powerup, **kwargs):
        super().__init__(**kwargs)
        self.mover = mover
        self.projectile_type = projectile_type
        self.fire_freq = fire_freq
        self.time_since_last_fire = self.fire_freq
        self.score = 0
        self.kills = 0
        self.waypoints = 0
        self.death_callbacks = []
        self.shot_sound = shot_sound
        self.waypoint = waypoint
        self.waypoint.visible = False
        self.waypoint.set_enter_callback(self.place_waypoint)
        self.powerup = powerup
        self.powerup.visible = False
        self.__powerup_arrow = None
        self.__waypoint_arrow = None
        self.__shield = None

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
            self.place_powerup()

    def attach(self, game_object, offset, take_parent_transform):
        """Attaches a game object to this game object at the give offset."""
        super().attach(game_object, offset, take_parent_transform)
        if isinstance(game_object, PowerupArrow):
            self.__powerup_arrow = game_object
            self.__powerup_arrow.pointee = self.powerup
        elif isinstance(game_object, NavArrow):
            self.__waypoint_arrow = game_object
            self.__waypoint_arrow.pointee = self.waypoint
        elif isinstance(game_object, Shield):
            self.__shield = game_object

    def set_velocity(self, velocity):
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
        self.powerup.die(None)
        for callback in self.death_callbacks:
            callback()

    def set_waypoint(self, waypoint):
        """Sets the waypoint the ship should go to."""
        self.waypoint = waypoint
        self.__waypoint_arrow.set_pointee(waypoint)
        # for attachment in self.attachments:
        #     try:
        #         attachment.game_object.set_pointee(waypoint)
        #     except AttributeError:
        #         pass

    def set_powerup(self, powerup: GameObject):
        self.__powerup_arrow.set_pointee(powerup)

    def place_waypoint(self, gob=None):
        angle = numpy.deg2rad(random.randrange(0, 360))
        pos = self.position + self.waypoint.distance * pygame.Vector2(numpy.cos(angle), numpy.sin(angle))
        self.waypoint.position = pos
        if gob:
            # The presence of a valid gob indicates we're here as a result of a collision
            self.waypoints += 1
        self.waypoint.set_number(self.waypoints + 1)

    def place_powerup(self):
        angle = numpy.deg2rad(random.randrange(0, 360))
        pos = self.position + self.powerup.distance * pygame.Vector2(numpy.cos(angle), numpy.sin(angle))
        self.powerup.position = pos
        self.powerup.visible = True

    def take_damage(self, damage, instigator):
        """Takes damage for this game object."""
        if not self.__god_mode:
            super().take_damage(damage, instigator)

    @property
    def shield(self) -> GameObject:
      return self.__shield

    @shield.setter
    def shield(self, shield: GameObject):
        # Find the shield attachment
        shield_attachments = [a for a in self.attachments if isinstance(a.game_object, Shield)]
        assert(len(shield_attachments) == 1)
        shield_attachments[0].game_object = shield
        self.__shield = shield


ConsoleRegistrar.register("god", Ship.toggle_god_mode)
