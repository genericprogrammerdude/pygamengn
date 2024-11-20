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

    class VertAlign(Enum):
        TOP = "TOP"
        CENTRE = "CENTRE"
        BOTTOM = "BOTTOM"

    class HorzAlign(Enum):
        LEFT = "LEFT"
        CENTRE = "CENTRE"
        RIGHT = "RIGHT"

    def __init__(self,
        horz_align = HorzAlign.LEFT,
        vert_align = VertAlign.TOP,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._horz_align = Panel.HorzAlign(horz_align)
        self._vert_align = Panel.VertAlign(vert_align)
        self._surface = None
        self._surface_changed = True

    def update(self, delta: int) -> bool:
        needs_redraw = self._needs_redraw
        needs_reblit = self._needs_reblit
        self._reset_reblit_flags()
        if needs_redraw:
            self._draw_surface()
            self._align()
            self._reset_redraw_flags()
        return super().update(delta) or needs_redraw or needs_reblit

    def resize_to_parent(self, parent_rect: pygame.rect):
        super().resize_to_parent(parent_rect)
        self._parent_rect_changed = True

    @abstractmethod
    def _draw_surface(self):
        pass

    def _align(self):
        """
        Aligns the panel's surface.

        When an alignment different than TOP and LEFT is set, _normalized_pos is used to adjust the actual position
        of the component within its parent rectangle starting from the alignment point.
        """
        # Horizontal alignment
        if self._horz_align == Panel.HorzAlign.LEFT:
            pass
        elif self._horz_align == Panel.HorzAlign.CENTRE:
            self._rect.x = (self._parent_rect.width - self._surface.get_rect().width) / 2
            self._rect.x += self._parent_rect.width * self._normalized_pos.x
        elif self._horz_align == Panel.HorzAlign.RIGHT:
            self._rect.x = self._parent_rect.width - self._surface.get_rect().width
            self._rect.x += self._parent_rect.width * self._normalized_pos.x
        # Vertical alignment
        if self._vert_align == Panel.VertAlign.TOP:
            pass
        elif self._vert_align == Panel.VertAlign.CENTRE:
            self._rect.y = (self._parent_rect.height - self._surface.get_rect().height) / 2
            self._rect.y += self._parent_rect.width * self._normalized_pos.y
        elif self._vert_align == Panel.VertAlign.BOTTOM:
            self._rect.y = self._parent_rect.height - self._surface.get_rect().height
            self._rect.y += self._parent_rect.width * self._normalized_pos.y

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
        corner_radii: CornerRadii = None,
        corner_radius: float = None,
        border_width: float = 0,
        border_colour = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.__colour = tuple(colour)
        self.__hover_colour = tuple(hover_colour) if hover_colour else self.__colour
        self.__corner_radii = corner_radii
        self.__corner_radius = corner_radius
        self.__border_width = border_width
        self.__border_colour = border_colour
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
        draw_border = self.__border_width != 0 and self.__border_colour

        if not self.__corner_radii and not self.__corner_radius:
            surface.fill(colour)
            if draw_border:
                min_dimension = min(self._rect.width, self._rect.height)
                pygame.draw.rect(
                    surface = surface,
                    color = self.__border_colour,
                    rect = pygame.Rect(0, 0, self._rect.width, self._rect.height),
                    width = round(min_dimension * self.__border_width)
                )
        else:

            min_dimension = min(self._rect.width, self._rect.height)
            rect = pygame.Rect(0, 0, self._rect.width, self._rect.height)
            # corner_radii takes precedence over corner_radius
            if self.__corner_radii:
                pygame.draw.rect(
                    surface = surface,
                    color = colour,
                    rect = rect,
                    border_top_left_radius = round(min_dimension * self.__corner_radii.top_left),
                    border_top_right_radius = round(min_dimension * self.__corner_radii.top_right),
                    border_bottom_right_radius = round(min_dimension * self.__corner_radii.bottom_right),
                    border_bottom_left_radius = round(min_dimension * self.__corner_radii.bottom_left)
                )
                if draw_border:
                    pygame.draw.rect(
                        surface = surface,
                        color = self.__border_colour,
                        rect = rect,
                        border_top_left_radius = round(min_dimension * self.__corner_radii.top_left),
                        border_top_right_radius = round(min_dimension * self.__corner_radii.top_right),
                        border_bottom_right_radius = round(min_dimension * self.__corner_radii.bottom_right),
                        border_bottom_left_radius = round(min_dimension * self.__corner_radii.bottom_left),
                        width = round(min_dimension * self.__border_width)
                    )
            else:
                pygame.draw.rect(
                    surface = surface,
                    color = colour,
                    rect = rect,
                    border_radius = round(min_dimension * self.__corner_radius)
                )
                if draw_border:
                    pygame.draw.rect(
                        surface = surface,
                        color = self.__border_colour,
                        rect = rect,
                        border_radius = round(min_dimension * self.__corner_radius),
                        width = round(min_dimension * self.__border_width)
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



@ClassRegistrar.register("TexturePanel")
class TexturePanel(Panel):
    """Basic UI panel that shows an image."""

    def __init__(self, image_asset, **kwargs):
        super().__init__(**kwargs)
        self._image_asset = image_asset

    def _draw_surface(self):
        super()._draw_surface()
        self._surface = pygame.transform.smoothscale(self._image_asset, self.rect.size)
