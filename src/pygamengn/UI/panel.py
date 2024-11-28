from abc import abstractmethod
from enum import Enum

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
        self._pos_changed = True
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

    def resize_to_parent(self, parent_rect: pygame.Rect):
        super().resize_to_parent(parent_rect)
        self._parent_rect_changed = True


    @property
    def normalized_pos(self) -> pygame.Vector2:
        return self._normalized_pos


    @normalized_pos.setter
    def normalized_pos(self, normalized_pos: pygame.Vector2):
        """Sets the normalized position for the component."""
        if normalized_pos != self._normalized_pos:
            self._normalized_pos = normalized_pos
            self._pos_changed = True


    @property
    def horz_align(self) -> HorzAlign:
        return self._horz_align


    @horz_align.setter
    def horz_align(self, horz_align: HorzAlign):
        """Sets the horizontal alignment for the component."""
        if horz_align != self._horz_align:
            self._horz_align = horz_align
            self._pos_changed = True


    @property
    def vert_align(self) -> VertAlign:
        return self._vert_align


    @vert_align.setter
    def vert_align(self, vert_align: VertAlign):
        """Sets the horizontal alignment for the component."""
        if vert_align != self._vert_align:
            self._vert_align = vert_align
            self._pos_changed = True


    @property
    def normalized_pos(self) -> pygame.Vector2:
        return self._normalized_pos


    @normalized_pos.setter
    def normalized_pos(self, normalized_pos: pygame.Vector2):
        """Sets the normalized position for the component."""
        if normalized_pos != self._normalized_pos:
            self._normalized_pos = normalized_pos
            self._pos_changed = True


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
        return self._pos_changed

    def _reset_reblit_flags(self):
        self._pos_changed = False
