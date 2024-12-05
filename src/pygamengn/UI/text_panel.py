import logging
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.UI.panel import Panel
from pygamengn.UI.font_asset import FontAsset



@ClassRegistrar.register("TextPanel")
class TextPanel(Panel):
    """Panel that sets its size to the size of the text in it. This panel ignores the parent rect."""

    def __init__(
        self,
        font_asset: FontAsset,
        text_colour: tuple[int],
        shadow_colour: tuple[int] = None,
        text: str = "",
        auto_font_size: bool = False,
        auto_font_size_factor: float = 1.0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.__font_asset = font_asset
        self.__text_colour = text_colour
        self.__shadow_colour = shadow_colour
        self.__text = text
        self.__auto_font_size = auto_font_size
        self.__auto_font_size_factor = auto_font_size_factor
        self.__text_changed = False
        self.__font_size = 0


    def _adjust_rect(self):
        redraw = self._surface is None
        if self.__auto_font_size and self.__text != "":
            font_size = self.__font_asset.get_font_size(self.__text, self.get_desired_rect_size())
            if font_size != self.__font_size:
                self.__font_size = font_size
                redraw = True

        if redraw:
            self._draw_surface()
            self._reset_redraw_flags()

        surface_rect = self._surface.get_rect()
        self._rect.update(self._rect.topleft, (surface_rect.width, surface_rect.height))
        self._align()


    def _draw_surface(self):
        """TextPanel ignores its parent rect and renders to the font size."""
        super()._draw_surface()
        self._surface = self.__font_asset.render(
            text = self.__text,
            text_colour = self.__text_colour,
            shadow_colour = self.__shadow_colour,
            font_size = self.__font_size
        )
        surface_rect = self._surface.get_rect()
        self._rect.update(self._rect.topleft, (surface_rect.width, surface_rect.height))


    @property
    def _needs_redraw(self) -> bool:
        return super()._needs_redraw or self.__text_changed


    def _reset_redraw_flags(self):
        super()._reset_redraw_flags()
        self.__text_changed = False


    @property
    def text(self) -> str:
        return self.__text


    @text.setter
    def text(self, text: str):
        if self.__text != text:
            self.__text = text
            self.__text_changed = True
            if self.__auto_font_size:
                self.__font_size = self.__font_asset.get_font_size( self.__text, self.get_desired_rect_size())


    @property
    def font_asset(self) -> FontAsset:
        return self.__font_asset


    @property
    def font_size(self) -> int:
        return self.__font_size


    @font_size.setter
    def font_size(self, font_size: int):
        if font_size != self.__font_size:
            self.__font_size = font_size
            self.__text_changed = True


    def get_desired_rect_size(self):
        """Returns the panel's desired rect size as opposed to its current one."""
        factor = self.__auto_font_size_factor if self.__auto_font_size else 1.0
        return pygame.Vector2(
            self._parent_rect.width * self.normalized_size.x * factor,
            self._parent_rect.height * self.normalized_size.y * factor
        )
