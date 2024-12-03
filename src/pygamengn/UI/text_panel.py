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


    def resize_to_parent(self, parent_rect: pygame.Rect):
        super().resize_to_parent(parent_rect)
        if self.__auto_font_size and self.__text != "":
            self.__font_size = self.__font_asset.get_font_size(
                self.__text, pygame.Vector2(self._rect.size) * self.__auto_font_size_factor
            )


    def _draw_surface(self):
        """TextPanel ignores its parent rect and renders to the font size."""
        super()._draw_surface()
        self._surface = self.__font_asset.render(
            text = self.__text,
            text_colour = self.__text_colour,
            shadow_colour = self.__shadow_colour,
            font_size = self.__font_size
        )
        self._align()


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
                self.__font_size = self.__font_asset.get_font_size(
                    self.__text, pygame.Vector2(self._rect.size) * self.__auto_font_size_factor
                )


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
