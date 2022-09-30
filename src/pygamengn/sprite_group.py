import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase


@ClassRegistrar.register("SpriteGroup")
class SpriteGroup(pygame.sprite.Group, GameObjectBase):
    """Class to make pygame Groups loadable as assets."""
