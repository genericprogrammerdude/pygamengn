import logging
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.UI.panel import Panel



@ClassRegistrar.register("TextPanel")
class TextPanel(Panel):
    """Panel that sets its size to the size of the text in it. This panel ignores the parent rect."""

    def __init__(
        self,
        font_asset,
        text_colour,
        shadow = False,
        shadow_colour = (0, 0, 0),
        text=" ",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.__font_asset = font_asset
        self.__text_colour = text_colour
        self.__shadow = shadow
        self.__shadow_colour = shadow_colour
        self.__text = text
        self.__text_changed = False


    def _draw_surface(self):
        """TextPanel ignores its parent rect and renders to the font size."""
        super()._draw_surface()
        if self.__shadow:
            shadow_surf = self.__font_asset.font.render(self.__text, True, self.__shadow_colour)
            front_surf = self.__font_asset.font.render(self.__text, True, self.__text_colour)
            dest = -0.06 * shadow_surf.get_rect().height
            shadow_surf.blit(front_surf, (dest, dest))
            self._surface = shadow_surf
        else:
            self._surface = self.__font_asset.font.render(self.__text, True, self.__text_colour)
        self._align()


    @property
    def text(self) -> str:
        return self.__text


    @text.setter
    def text(self, text: str):
        if self.__text != text:
            self.__text = text
            self.__text_changed = True


    @property
    def _needs_redraw(self) -> bool:
        return super()._needs_redraw or self.__text_changed


    def _reset_redraw_flags(self):
        super()._reset_redraw_flags()
        self.__text_changed = False
