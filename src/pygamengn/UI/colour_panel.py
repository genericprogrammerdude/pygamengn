import logging
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase
from pygamengn.UI.panel import Panel



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
        self.__border_changed = False


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


    @property
    def _needs_redraw(self) -> bool:
        return super()._needs_redraw or self.__border_changed


    def _reset_redraw_flags(self):
        super()._reset_redraw_flags()
        self.__border_changed = False


    def set_border(self, normalized_width: float, colour: tuple[int]):
        if normalized_width != self.__border_width and colour != self.__border_colour:
            self.__border_width = normalized_width
            self.__border_colour = colour
            self.__border_changed = True
