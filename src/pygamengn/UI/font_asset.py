import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase


@ClassRegistrar.register("FontAsset")
class FontAsset(GameObjectBase):
    """Loadable font asset."""

    def __init__(self, fname, size):
        self.font = pygame.font.Font(fname, size)
