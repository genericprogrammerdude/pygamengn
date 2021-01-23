import pygame

from class_registrar import ClassRegistrar
from game_object import GameObject


@ClassRegistrar.register("Trigger")
class Trigger(GameObject):
    """A trigger triggers actions when game objects enter them."""

    def __init__(self, enter_sound=None, **kwargs):
        super().__init__(**kwargs)
        self.enter_sound = enter_sound
        self.enter_callback = None
        self.exit_callback = None
        self.gobs_in_trigger = []

    def update(self, delta):
        super().update(delta)

        # TODO: This is a very expensive way to keep track of gobs in the Trigger and avoid calling enter callback
        # more than once
        for index, gob in enumerate(self.gobs_in_trigger):
            if gob and gob.alive():
                collision = pygame.sprite.collide_mask(gob, self)
                if collision is None:
                    if self.exit_callback:
                        self.exit_callback(gob)
                    del self.gobs_in_trigger[index]

    def handle_collision(self, gob, world_pos):
        """Reacts to collision against game object gob."""
        # Apply damage to the collided sprite
        if self.enter_callback:
            if not gob in self.gobs_in_trigger:
                if self.enter_sound:
                    self.enter_sound.play()
                self.gobs_in_trigger.append(gob)
                self.enter_callback(gob)

    def set_enter_callback(self, enter_callback):
        """Sets the callback to invoke when a game object enters the trigger."""
        self.enter_callback = enter_callback

    def set_exit_callback(self, exit_callback):
        """Sets the callback to invoke when a game object exits the trigger."""
        self.exit_callback = exit_callback

    def take_damage(self, damage, instigator):
        # Triggers handle collisions but don't take damage
        pass
