import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase


@ClassRegistrar.register("FontAsset")
class FontAsset(GameObjectBase):
    """Loadable font asset."""

    def __init__(self, fname: str, size: int):
        self.__font = pygame.font.Font(fname, size)

    def render(self, text: str, colour: tuple[int]) -> pygame.Surface:
        surface = self.__font.render(text, True, colour)
        return surface
