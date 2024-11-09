from enum import Enum

import logging
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.UI.ui_base import UIBase


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
        logging.info(f"{self.name}.resize() generated new image")

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

    def __init__(
        self,
        font_asset,
        text_colour,
        horz_align = "LEFT",
        vert_align = "TOP",
        shadow = False,
        shadow_colour = (0, 0, 0),
        text=" ",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.font_asset = font_asset
        self.text_colour = text_colour
        self.horz_align = TextPanel.HorzAlign(horz_align)
        self.vert_align = TextPanel.VertAlign(vert_align)
        self.shadow = shadow
        self.shadow_colour = shadow_colour
        self.text = text
        self.__text_is_dirty = True

    def set_text(self, text):
        if self.text != text:
            self.text = text
            self.__text_is_dirty = True

    def resize(self):
        """TextPanel ignores its parent rect and renders to the font size."""
        if self.__text_is_dirty:
            if self.shadow:
                shadow_surf = self.font_asset.font.render(self.text, True, self.shadow_colour)
                front_surf = self.font_asset.font.render(self.text, True, self.text_colour)
                dest = -0.06 * shadow_surf.get_rect().height
                shadow_surf.blit(front_surf, (dest, dest))
                self.image = shadow_surf
            else:
                self.image = self.font_asset.font.render(self.text, True, self.text_colour)
            self.__align()
            self.__text_is_dirty = False
            logging.info(f"{self.name}.resize() generated new image")

    def update(self, parent_rect: pygame.rect, delta: int):
        super().update(parent_rect, delta)
        self.__align()

    def _needs_redraw(self, parent_rect: pygame.rect) -> bool:
        return self.__text_is_dirty

    def __align(self):
        """Aligns the text image."""
        # Horizontal alignment
        if self.horz_align == TextPanel.HorzAlign.LEFT:
            pass  # This is what UIBase does by default
        elif self.horz_align == TextPanel.HorzAlign.CENTRE:
            self.rect.x = self.parent_rect.x + (self.parent_rect.width - self.image.get_rect().width) / 2
            self.rect.x += self.parent_rect.width * self.pos.x
        elif self.horz_align == TextPanel.HorzAlign.RIGHT:
            self.rect.x = self.parent_rect.x + self.parent_rect.width - self.image.get_rect().width
            self.rect.x += self.parent_rect.width * self.pos.x
        # Vertical alignment
        if self.vert_align == TextPanel.VertAlign.TOP:
            pass  # This is what UIBase does by default
        elif self.vert_align == TextPanel.VertAlign.CENTRE:
            self.rect.y = self.parent_rect.y + (self.parent_rect.height - self.image.get_rect().height) / 2
            self.rect.y += self.parent_rect.width * self.pos.y
        elif self.vert_align == TextPanel.VertAlign.BOTTOM:
            self.rect.y = self.parent_rect.y + self.parent_rect.height - self.image.get_rect().height
            self.rect.y += self.parent_rect.width * self.pos.y
