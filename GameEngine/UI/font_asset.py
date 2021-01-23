import pygame

from class_registrar import ClassRegistrar
from game_object_base import GameObjectBase


@ClassRegistrar.register("FontAsset")
class FontAsset(GameObjectBase):
    """Loadable font asset."""

    def __init__(self, font_fname, size):
        self.font = pygame.font.Font(font_fname, size)
