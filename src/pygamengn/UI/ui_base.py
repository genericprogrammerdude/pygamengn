from abc import abstractmethod

import logging
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase
from pygamengn.interpolator import Interpolator


@ClassRegistrar.register("UIBase")
class UIBase(GameObjectBase):
    """Base class for UI components."""

    def __init__(self, pos, size, children, fix_aspect_ratio, name="", **kwargs):
        super().__init__(**kwargs)
        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.children = children
        self.fix_aspect_ratio = fix_aspect_ratio
        self.name = name
        self.parent_rect = None
        self.rect = None
        self.image = None
        self.aspect_ratio = None
        self._is_dirty = True
        self.__bind_children()
        self.__fade_out_interp = None
        self.__fade_out_time = 0

    def update(self, parent_rect: pygame.rect, delta: int):
        """Updates the UI component and its children."""
        if self.is_dirty():
            self._resize_to_parent(parent_rect)
            self._is_dirty = False

        if self._needs_redraw(parent_rect):
            self.resize()

        for child in self.children:
            child.update(self.rect, delta)

        if self.__fade_out_interp and self.image:
            interp_value = self.__fade_out_interp.get(self.__fade_out_time)
            self.__fade_out_time += delta
            self.image.set_alpha(interp_value)
            for child in self.children:
                if child.image:
                    child.image.set_alpha(interp_value)

    def set_position(self, new_normalized_pos: pygame.Vector2):
        if self.pos != new_normalized_pos:
            self._is_dirty = True
            self.pos = new_normalized_pos
            for child in self.children:
                child._is_dirty = True

    def fade_out(self, duration: int):
        self.__fade_out_interp = Interpolator(duration = duration, from_value = 255, to_value = 0)
        self.__fade_out_time = 0

    def _needs_redraw(self, parent_rect: pygame.rect) -> bool:
        return not self.image or not self.parent_rect or parent_rect.size != self.parent_rect.size

    def _resize_to_parent(self, parent_rect):
        """Resizes the component's rect to match size with its parent's rect."""
        width = parent_rect.width * self.size[0]
        height = parent_rect.height * self.size[1]
        if self.fix_aspect_ratio:
            if self.aspect_ratio is None:
                self.aspect_ratio = width / height
            if width / self.aspect_ratio > height:
                # Height is the limiting factor
                width = self.aspect_ratio * height
            elif height * self.aspect_ratio > width:
                # Width is the limiting factor
                height = width / self.aspect_ratio
        pos = parent_rect.topleft + pygame.Vector2(parent_rect.width * self.pos[0], parent_rect.height * self.pos[1])
        self.rect = pygame.Rect(pos.x, pos.y, width, height)
        self.parent_rect = parent_rect
        self._is_dirty = False

    def is_dirty(self):
        """
        Returns whether the component needs to be resized. Returning True guarantees the component will be re-drawn.
        """
        return self._is_dirty

    def propagate_mouse_pos(self, pos) -> bool:
        """Tells the component and its children the position of the mouse pointer in screen coordinates."""
        capture_hover = False
        for child in self.children:
            capture_hover = capture_hover or child.propagate_mouse_pos(pos)

        if capture_hover:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return capture_hover

    def __bind_children(self, parent=None):
        """Binds children to class members to make them accessible."""
        if not parent:
            parent = self
        for child in self.children:
            child.__bind_children(parent)
            if child.name:
                try:
                    a = getattr(parent, child.name)
                    logging.warn(f"{child.name} attr is already assigned with {child}. Not assigning it {a}")
                except AttributeError:
                    setattr(parent, child.name, child)

    @abstractmethod
    def resize(self):
        """Called when the component resized its own rect to match its parent's rect."""
        pass
