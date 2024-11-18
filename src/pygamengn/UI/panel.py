from abc import abstractmethod
from enum import Enum

import logging
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase
from pygamengn.UI.component import Component



@ClassRegistrar.register("Panel")
class Panel(Component):
    """Basic UI panel that keeps an image with its visual contents."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._surface = None
        self._surface_changed = True

    def update(self, delta: int) -> bool:
        needs_redraw = self._needs_redraw
        needs_reblit = self._needs_reblit
        self._reset_reblit_flags()
        if needs_redraw:
            self._draw_surface()
            self._reset_redraw_flags()
            logging.debug(f"{self.name} drew a new image")
        return super().update(delta) or needs_redraw or needs_reblit

    @abstractmethod
    def _draw_surface(self):
        pass

    @property
    def _blit_surface(self) -> pygame.Surface:
        """Returns the image that the UI component wants to blit to the screen."""
        return self._surface

    @property
    def _needs_redraw(self) -> bool:
        return self._parent_rect_changed

    def _reset_redraw_flags(self):
        self._parent_rect_changed = False

    @property
    def _needs_reblit(self) -> bool:
        return False

    def _reset_reblit_flags(self):
        pass



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
        self.__mouse_is_hovering_changed = False
        self.__hover_surface = None


    @property
    def _blit_surface(self) -> pygame.Surface:
        """Returns the surface that the UI component wants to blit to the screen."""
        super()._blit_surface
        return self.__hover_surface if self.__mouse_is_hovering else self._surface


    def _draw_surface(self):
        super()._draw_surface()
        self._surface = self.__draw_colour_surface(self.__colour)
        self.__hover_surface = self.__draw_colour_surface(self.__hover_colour)


    def __draw_colour_surface(self, colour: tuple[int]) -> pygame.Surface:
        surface = pygame.Surface(self._rect.size, pygame.SRCALPHA)
        if not self.__corner_radii and not self.__corner_radius:
            surface.fill(colour)
        else:
            min_dimension = min(self._rect.width, self._rect.height)
            # corner_radii takes precedence over corner_radius
            if self.__corner_radii:
                pygame.draw.rect(
                    surface = surface,
                    color = colour,
                    rect = pygame.Rect(0, 0, self._rect.width, self._rect.height),
                    border_top_left_radius = round(min_dimension * self.__corner_radii.top_left),
                    border_top_right_radius = round(min_dimension * self.__corner_radii.top_right),
                    border_bottom_right_radius = round(min_dimension * self.__corner_radii.bottom_right),
                    border_bottom_left_radius = round(min_dimension * self.__corner_radii.bottom_left)
                )
            else:
                pygame.draw.rect(
                    surface = surface,
                    color = colour,
                    rect = pygame.Rect(0, 0, self._rect.width, self._rect.height),
                    border_radius = round(min_dimension * self.__corner_radius)
                )
        return surface


    def process_mouse_event(self, pos: pygame.Vector2, event_type: int) -> bool:
        capture_event = super().process_mouse_event(pos, event_type)

        if event_type == pygame.MOUSEMOTION and self.__colour != self.__hover_colour:
            # Special handling of MOUSEMOTION event to honour self.__hover_colour
            local_pos = pos - pygame.Vector2(self._parent_rect.topleft)
            if self._rect.collidepoint(local_pos):
                if not self.__mouse_is_hovering:
                    self.__mouse_is_hovering = True
                    self.__mouse_is_hovering_changed = True
            else:
                if self.__mouse_is_hovering:
                    self.__mouse_is_hovering = False
                    self.__mouse_is_hovering_changed = True

        return capture_event


    @property
    def _needs_reblit(self) -> bool:
        return self.__mouse_is_hovering_changed


    def _reset_reblit_flags(self):
        self.__mouse_is_hovering_changed = False



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
        self.__align()


    def __align(self):
        """Aligns the text surface."""
        # Horizontal alignment
        if self.__horz_align == TextPanel.HorzAlign.LEFT:
            pass  # This is what Component does by default
        elif self.__horz_align == TextPanel.HorzAlign.CENTRE:
            self._rect.x = (self._parent_rect.width - self._surface.get_rect().width) / 2
            self._rect.x += self._parent_rect.width * self._normalized_pos.x
        elif self.__horz_align == TextPanel.HorzAlign.RIGHT:
            self._rect.x = self._parent_rect.width - self._surface.get_rect().width
            self._rect.x += self._parent_rect.width * self._normalized_pos.x
        # Vertical alignment
        if self.__vert_align == TextPanel.VertAlign.TOP:
            pass  # This is what Component does by default
        elif self.__vert_align == TextPanel.VertAlign.CENTRE:
            self._rect.y = (self._parent_rect.height - self._surface.get_rect().height) / 2
            self._rect.y += self._parent_rect.width * self._normalized_pos.y
        elif self.__vert_align == TextPanel.VertAlign.BOTTOM:
            self._rect.y = self._parent_rect.height - self._surface.get_rect().height
            self._rect.y += self._parent_rect.width * self._normalized_pos.y


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



@ClassRegistrar.register("TexturePanel")
class TexturePanel(Panel):
    """Basic UI panel that shows an image."""

    def __init__(self, image_asset, **kwargs):
        super().__init__(**kwargs)
        self._image_asset = image_asset

    def _draw_surface(self):
        super()._draw_surface()
        self._surface = pygame.transform.smoothscale(self._image_asset, self.rect.size)
