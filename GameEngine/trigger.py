import pygame

from game_object import GameObject
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Trigger")
class Trigger(GameObject):
    """A trigger triggers actions when game objects enter them."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enter_callback = None

    def handle_collision(self, gob, world_pos):
        """Reacts to collision against game object gob."""
        # Apply damage to the collided sprite
        if self.enter_callback:
            self.enter_callback(gob)

    def set_enter_callback(self, enter_callback):
        """Sets the callback to invoke when a game object enters the trigger."""
        self.enter_callback = enter_callback

    def take_damage(self, damage, instigator):
        """Takes damage for this game object."""
        pass
