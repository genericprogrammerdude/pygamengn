from enum import Enum

import pygame

from pygamengn.UI.ui_base import UIBase
from pygamengn.class_registrar import ClassRegistrar


@ClassRegistrar.register("Panel")
class Panel(UIBase):
    """Basic UI panel that shows an image."""

    def __init__(self, image_asset, **kwargs):
        super().__init__(**kwargs)
        self.image_asset = image_asset
        rect = image_asset.get_rect()
        self.aspect_ratio = rect.width / rect.height

    def resize(self):
        """Resizes the image to match the panel's size with its parent's rect."""
        self.image = pygame.transform.scale(self.image_asset, self.rect.size)


@ClassRegistrar.register("ColourPanel")
class ColourPanel(UIBase):
    """Basic UI panel that is a solid colour and has no image."""

    def __init__(self, colour, hover_colour=None, corner_radius=0, **kwargs):
        super().__init__(**kwargs)
        self.colour = tuple(colour)
        self.corner_radius = corner_radius
        self.__mouse_is_hovering = False
        self.__needs_redraw = True
        if hover_colour:
            self.hover_colour = tuple(hover_colour)
        else:
            self.hover_colour = self.colour

    def resize(self):
        """Resizes the image to match the panel's size with its parent's rect."""
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.__build_image(self.hover_colour if self.__mouse_is_hovering else self.colour)

    def propagate_mouse_pos(self, pos) -> bool:
        """Notifies the component that the mouse is hovering over it."""
        capture_hover = super().propagate_mouse_pos(pos)
        if self.colour != self.hover_colour:
            if self.rect.collidepoint(pos):
                capture_hover = True
                if not self.__mouse_is_hovering and self.hover_colour != self.colour:
                    self.__needs_redraw = True
                    self.__mouse_is_hovering = True
            else:
                if self.__mouse_is_hovering and self.hover_colour != self.colour:
                    self.__needs_redraw = True
                    self.__mouse_is_hovering = False
        return capture_hover

    def _needs_redraw(self, parent_rect: pygame.rect) -> bool:
        return self.__needs_redraw

    def __build_image(self, colour):
        if self.corner_radius == 0:
            self.image.fill(colour)
        else:
            pygame.draw.rect(
                surface = self.image,
                color = colour,
                rect = pygame.Rect(0, 0, self.rect.width, self.rect.height),
                border_radius = round(min(self.rect.width, self.rect.height) * self.corner_radius)
            )
        self.__needs_redraw = False


@ClassRegistrar.register("TextPanel")
class TextPanel(UIBase):
    """Panel that sets its size to the size of the text in it. This panel ignores the parent rect."""

    class VertAlign(Enum):
        TOP = "TOP"
        CENTRE = "CENTRE"
        BOTTOM = "BOTTOM"

    class HorzAlign(Enum):
        LEFT = "LEFT"
        CENTRE = "CENTRE"
        RIGHT = "RIGHT"

    def __init__(self, font_asset, text_colour, horz_align, vert_align, text=" ", **kwargs):
        super().__init__(**kwargs)
        self.font_asset = font_asset
        self.text_colour = text_colour
        self.horz_align = TextPanel.HorzAlign(horz_align)
        self.vert_align = TextPanel.VertAlign(vert_align)
        self.text = text
        self.__text_is_dirty = True

    def set_text(self, text):
        if self.text != text:
            self.text = text
            self.__text_is_dirty = True

    def resize(self):
        """TextPanel ignores its parent rect and renders to the font size."""
        if self.__text_is_dirty:
            self.image = self.font_asset.font.render(self.text, True, self.text_colour)
            self.__align()
            self.__text_is_dirty = False

    def _needs_redraw(self, parent_rect: pygame.rect) -> bool:
        return self.__text_is_dirty

    def __align(self):
        """Aligns the text image."""
        # Horizontal alignment
        if self.horz_align == TextPanel.HorzAlign.LEFT:
            pass  # This is what UIBase does by default
        elif self.horz_align == TextPanel.HorzAlign.CENTRE:
            self.rect.x = self.parent_rect.x + (self.parent_rect.width - self.image.get_rect().width) / 2
        elif self.horz_align == TextPanel.HorzAlign.RIGHT:
            self.rect.x = self.parent_rect.x + self.parent_rect.width - self.image.get_rect().width
        # Vertical alignment
        if self.vert_align == TextPanel.VertAlign.TOP:
            pass  # This is what UIBase does by default
        elif self.vert_align == TextPanel.VertAlign.CENTRE:
            self.rect.y = self.parent_rect.y + (self.parent_rect.height - self.image.get_rect().height) / 2
        elif self.vert_align == TextPanel.VertAlign.BOTTOM:
            self.rect.y = self.parent_rect.y + self.rect.parent_height - self.image.get_rect().height

    @classmethod
    def scale_to_fit(cls, size, max_size):
        """Scales a rectangle size down to fit max_size maintaining the original aspect ratio."""
        width = size[0]
        height = size[1]
        scale_x = max_size[0] / width
        scale_y = max_size[1] / height

        if scale_x < 1 or scale_y < 1:
            aspect_ratio = width / height
            if scale_x < scale_y:
                width = max_size[0]
                height = width / aspect_ratio
            else:
                height = max_size[1]
                width = height * aspect_ratio

        return (round(width), round(height))
