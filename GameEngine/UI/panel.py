from enum import Enum

import pygame

from UI.font_asset import FontAsset
from UI.ui_base import UIBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Panel")
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


@GameObjectFactory.register("ColourPanel")
class ColourPanel(UIBase):
    """Basic UI panel that is a solid colour and has no image."""

    def __init__(self, colour, hover_colour=None, **kwargs):
        super().__init__(**kwargs)
        self.colour = tuple(colour)
        if hover_colour:
            self.hover_colour = tuple(hover_colour)
        else:
            self.hover_colour = self.colour

    def resize(self):
        """Resizes the image to match the panel's size with its parent's rect."""
        self.image = pygame.Surface(self.rect.size, pygame.HWSURFACE | pygame.SRCALPHA)
        self.image.fill(self.colour)

    def propagate_mouse_pos(self, pos):
        """Notifies the component that the mouse is hovering over it."""
        components = super().propagate_mouse_pos(pos)
        if self.colour != self.hover_colour:
            if self.rect.collidepoint(pos):
                components.append(self)
                if self.image.get_at((0, 0)) != self.hover_colour:
                    self.image.fill(self.hover_colour)
            else:
                if self.image.get_at((0, 0)) != self.colour:
                    self.image.fill(self.colour)
        return components


@GameObjectFactory.register("TextPanel")
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

    def __init__(self, font_asset, text_colour, horz_align, vert_align, text, **kwargs):
        super().__init__(**kwargs)
        self.font_asset = font_asset
        self.text_colour = text_colour
        self.horz_align = TextPanel.HorzAlign(horz_align)
        self.vert_align = TextPanel.VertAlign(vert_align)
        self.text = text
        self.text_is_dirty = True

    def set_text(self, text):
        self.text_is_dirty = (self.text != text)
        self.text = text

    def is_dirty(self):
        return self.text_is_dirty

    def resize(self):
        """TextPanel ignores its parent rect and renders to the font size."""
        self.image = self.font_asset.font.render(self.text, True, self.text_colour)
        image_size = self.image.get_rect().size
        if image_size[0] != self.parent_rect.size[0] or image_size[1] != self.parent_rect.size[1]:
            size = self.scale_to_fit(self.image.get_rect().size, self.parent_rect.size)
            self.image = pygame.transform.scale(self.image, size)
        self.text_is_dirty = False
        self.align()

    def align(self):
        """Aligns the text image."""
        # Horizontal alignment
        if self.horz_align == TextPanel.HorzAlign.LEFT:
            pass  # This is what UIBase does by default
        elif self.horz_align == TextPanel.HorzAlign.CENTRE:
            self.rect.x = self.rect.x + (self.rect.width - self.image.get_rect().width) / 2
        elif self.horz_align == TextPanel.HorzAlign.RIGHT:
            self.rect.x = self.rect.x + self.rect.width - self.image.get_rect().width
        # Vertical alignment
        if self.vert_align == TextPanel.VertAlign.TOP:
            pass  # This is what UIBase does by default
        elif self.vert_align == TextPanel.VertAlign.CENTRE:
            self.rect.y = self.rect.y + (self.rect.height - self.image.get_rect().height) / 2
        elif self.vert_align == TextPanel.VertAlign.BOTTOM:
            self.rect.y = self.rect.y + self.rect.height - self.image.get_rect().height

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
