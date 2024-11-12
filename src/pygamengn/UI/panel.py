from enum import Enum

import logging
import pygame

from abc import abstractmethod

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase
from pygamengn.UI.ui_base import UIBase



@ClassRegistrar.register("Panel")
class Panel(UIBase):
    """Basic UI panel that keeps an image with its visual contents."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._image = None
        self._needs_redraw = True


    def update(self, parent_rect: pygame.rect, delta: int):
        super().update(parent_rect, delta)
        if self._needs_redraw:
            self._draw()
            self._needs_redraw = False


    ### ACHTUNG!
    ### This is temporary! It should not be needed!
    @property
    def image(self):
        return self._image


    @abstractmethod
    def _draw(self):
        pass



@ClassRegistrar.register("TexturePanel")
class TexturePanel(UIBase):
    """Basic UI panel that shows an image."""

    def __init__(self, image_asset, **kwargs):
        super().__init__(**kwargs)
        self.image_asset = image_asset
        rect = image_asset.get_rect()
        self.aspect_ratio = rect.width / rect.height

    def resize(self):
        """Resizes the image to match the panel's size with its parent's rect."""
        self.image = pygame.transform.scale(self.image_asset, self._rect.size)



@ClassRegistrar.register("ColourPanel")
class ColourPanel(Panel):
    """Basic UI panel that is a solid colour and has no image."""

    @ClassRegistrar.register("CornerRadii")
    class CornerRadii(GameObjectBase):
        def __init__(self, top_left: float = 0, top_right: float = 0, bottom_right: float = 0, bottom_left: float = 0):
            self.top_left = top_left
            self.top_right = top_right
            self.bottom_right = bottom_right
            self.bottom_left = bottom_left

    def __init__(
        self,
        colour,
        hover_colour = None,
        corner_radii = None,
        corner_radius = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.__colour = tuple(colour)
        self.__hover_colour = tuple(hover_colour) if hover_colour else self.__colour
        self.__corner_radii = corner_radii
        self.__corner_radius = corner_radius
        self.__mouse_is_hovering = False


    def _draw(self):
        """Resizes the image to match the panel's size with its parent's rect."""
        logging.info(f"{self.name}: ColourPanel._draw() generated new image")
        self._image = pygame.Surface(self._rect.size, pygame.SRCALPHA)
        if not self.__corner_radii and not self.__corner_radius:
            self._image.fill(colour)
        else:
            colour = self.__hover_colour if self.__mouse_is_hovering else self.__colour
            min_dimension = min(self._rect.width, self._rect.height)
            # corner_radii takes precedence over corner_radius
            if self.__corner_radii:
                pygame.draw.rect(
                    surface = self._image,
                    color = colour,
                    rect = pygame.Rect(0, 0, self._rect.width, self._rect.height),
                    border_top_left_radius = round(min_dimension * self.__corner_radii.top_left),
                    border_top_right_radius = round(min_dimension * self.__corner_radii.top_right),
                    border_bottom_right_radius = round(min_dimension * self.__corner_radii.bottom_right),
                    border_bottom_left_radius = round(min_dimension * self.__corner_radii.bottom_left)
                )
            else:
                pygame.draw.rect(
                    surface = self._image,
                    color = colour,
                    rect = pygame.Rect(0, 0, self._rect.width, self._rect.height),
                    border_radius = round(min_dimension * self.__corner_radius)
                )


    def propagate_mouse_pos(self, pos) -> bool:
        """Notifies the component that the mouse is hovering over it."""
        capture_hover = super().propagate_mouse_pos(pos)
        if not capture_hover and self.__colour != self.__hover_colour:
            if self._rect.collidepoint(pos):
                capture_hover = True
                if not self.__mouse_is_hovering:
                    self._needs_redraw = True
                    self.__mouse_is_hovering = True
            else:
                if self.__mouse_is_hovering:
                    self._needs_redraw = True
                    self.__mouse_is_hovering = False
        return capture_hover



@ClassRegistrar.register("TextPanel")
class TextPanel(Panel):
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
        self.__font_asset = font_asset
        self.__text_colour = text_colour
        self.__horz_align = TextPanel.HorzAlign(horz_align)
        self.__vert_align = TextPanel.VertAlign(vert_align)
        self.__shadow = shadow
        self.__shadow_colour = shadow_colour
        self.__text = text


    def _draw(self):
        """TextPanel ignores its parent rect and renders to the font size."""
        logging.info(f"{self.name}: TextPanel._draw() generated new image")
        if self.__shadow:
            shadow_surf = self.__font_asset.font.render(self.__text, True, self.__shadow_colour)
            front_surf = self.__font_asset.font.render(self.__text, True, self.__text_colour)
            dest = -0.06 * shadow_surf.get_rect().height
            shadow_surf.blit(front_surf, (dest, dest))
            self._image = shadow_surf
        else:
            self._image = self.__font_asset.font.render(self.__text, True, self.__text_colour)
        self.__align()


    def __align(self):
        """Aligns the text image."""
        # Horizontal alignment
        if self.__horz_align == TextPanel.HorzAlign.LEFT:
            pass  # This is what UIBase does by default
        elif self.__horz_align == TextPanel.HorzAlign.CENTRE:
            self._rect.x = self._parent_rect.x + (self._parent_rect.width - self._image.get_rect().width) / 2
            self._rect.x += self._parent_rect.width * self._normalized_pos.x
        elif self.__horz_align == TextPanel.HorzAlign.RIGHT:
            self._rect.x = self._parent_rect.x + self._parent_rect.width - self._image.get_rect().width
            self._rect.x += self._parent_rect.width * self._normalized_pos.x
        # Vertical alignment
        if self.__vert_align == TextPanel.VertAlign.TOP:
            pass  # This is what UIBase does by default
        elif self.__vert_align == TextPanel.VertAlign.CENTRE:
            self._rect.y = self._parent_rect.y + (self._parent_rect.height - self._image.get_rect().height) / 2
            self._rect.y += self._parent_rect.width * self._normalized_pos.y
        elif self.__vert_align == TextPanel.VertAlign.BOTTOM:
            self._rect.y = self._parent_rect.y + self._parent_rect.height - self._image.get_rect().height
            self._rect.y += self._parent_rect.width * self._normalized_pos.y
