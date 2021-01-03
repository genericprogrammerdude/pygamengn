import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("SpriteGroup")
class SpriteGroup(pygame.sprite.Group, GameObjectBase):
    """Class to make pygame Groups loadable as assets."""
