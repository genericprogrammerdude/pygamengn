import pygame

from class_registrar import ClassRegistrar
from game_object_base import GameObjectBase


@ClassRegistrar.register("SpriteGroup")
class SpriteGroup(pygame.sprite.Group, GameObjectBase):
    """Class to make pygame Groups loadable as assets."""
