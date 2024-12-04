from __future__ import annotations

import logging

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase



@ClassRegistrar.register("FontAsset")
class FontAsset(GameObjectBase):
    """Loadable font asset."""

    """Default monospace font that is always available through FontAsset.monospace()."""
    __monospace_font_asset = None

    def __init__(self, fname: str, size: int):
        self.__fname = fname
        self.__size = size
        self.__fonts = {}
        self.__get_font(size)


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

        tight_dim = 1
        if (fit_size[0] / text_size[0]) < (fit_size[1] / text_size[1]):
            tight_dim = 0

        visited_sizes = []
        while abs(1 - text_size[tight_dim] / fit_size[tight_dim]) > 0.01 and not font_size in visited_sizes:
            font_size = round(font_size * fit_size[tight_dim] / text_size[tight_dim])
            text_size = self.__get_font(font_size).size(text)
            visited_sizes.append(font_size)
            tight_dim = 1
            if (fit_size[0] / text_size[0]) < (fit_size[1] / text_size[1]):
                tight_dim = 0

        return font_size


    def __get_font(self, size: int) -> pygame.font.Font:
        try:
            font = self.__fonts[size]
        except KeyError:
            try:
                font = pygame.font.Font(self.__fname, size)
            except (TypeError, RuntimeError) as e:
                font = pygame.font.SysFont(self.__fname, size)
                self.__fname = [font.name]
            self.__fonts[size] = font
            logging.debug(f"Added size {size} for {self.__fname}")

        return font


    @classmethod
    def monospace(cls) -> FontAsset:
        if cls.__monospace_font_asset is None:
            cls.__monospace_font_asset = FontAsset(
                # At least one of these _should_ be available in any platform
                fname = ["Consolas", "SF Mono", "DejaVu Sans Mono", "Roboto Mono", "Courier"],
                size = 12
            )
        return cls.__monospace_font_asset
