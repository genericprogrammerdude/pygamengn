import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("FontAsset")
class FontAsset(GameObjectBase):
    """Loadable font asset."""

    def __init__(self, font_fname, size):
        self.font = pygame.font.Font(font_fname, size)
