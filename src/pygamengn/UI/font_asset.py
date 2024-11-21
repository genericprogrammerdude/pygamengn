import logging

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase



@ClassRegistrar.register("FontAsset")
class FontAsset(GameObjectBase):
    """Loadable font asset."""

    def __init__(self, fname: str, size: int):
        self.__fname = fname
        self.__size = size
        self.__fonts = {
            size: pygame.font.Font(fname, size),
        }


    def render(
        self,
        text: str,
        text_colour: tuple[int],
        shadow_colour: tuple[int] = None,
        font_size: int = 0
    ) -> pygame.Surface:

        if font_size <= 0:
            font = self.__fonts[self.__size]
        else:
            font = self.__get_font(font_size)

        surface = font.render(text, True, text_colour)

        if shadow_colour:
            shadow_surface = font.render(text, True, shadow_colour)
            dest = -0.06 * surface.get_rect().height
            shadow_surface.blit(surface, (dest, dest))
            surface = shadow_surface

        return surface


    def get_font_size(self, text: str, fit_size: tuple[int]) -> int:
        font_size = self.__size
        text_size = self.__fonts[font_size].size(text)

        while font_size > 0 and (text_size[0] > fit_size[0] or text_size[1] > fit_size[1]):
            font_size -= 2
            text_size = self.__get_font(font_size).size(text)

        while text_size[0] < fit_size[0] and text_size[1] < fit_size[1]:
            font_size += 2
            text_size = self.__get_font(font_size).size(text)

        return font_size


    def __get_font(self, size: int) -> pygame.font.Font:
        try:
            font = self.__fonts[size]
        except KeyError:
            font = pygame.font.Font(self.__fname, size)
            self.__fonts[size] = font
            logging.info(f"Added size {size} for {self.__fname}")

        return font
