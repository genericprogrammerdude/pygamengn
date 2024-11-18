from __future__ import annotations
from abc import abstractmethod

import logging
import pygame

from pygamengn.blit_surface import BlitSurface
from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase



@ClassRegistrar.register("Component")
class Component(GameObjectBase):
    """
    Base class for UI components.

    This class takes care of administrative and basic geometric issues. Its functionality is limited to the following
    topics:
        1. Keep its own geometry updated to the geometry of its parent rectangle.
        2. Manage addition and removal of children.
        3. Keep children's geometry updated to any changes to its own geometry.
        4. Handle drawing of entire UI tree, from root to leaves.
        5. Handle mouse events.

    In addition, this class must always be instantiable as a parent container of other UI components that need to be
    kept together under a single parent, especially when the parent doesn't need to draw to the screen.
    """


    def __init__(
        self,
        pos = [0, 0],
        size = [1, 1],
        children = [],
        fix_aspect_ratio = False,
        name="",
        wanted_mouse_events = list[int],
        **kwargs
    ):
        super().__init__(**kwargs)
        self.__size = pygame.Vector2(size)
        self.__children = children
        self.__fix_aspect_ratio = fix_aspect_ratio
        self.__name = name
        self.__wanted_mouse_events = wanted_mouse_events
        self.__aspect_ratio = None
        self._normalized_pos = pygame.Vector2(pos)
        self._parent_rect = None
        self._parent_rect_changed = False
        self._rect = None


    def update(self, delta: int) -> bool:
        """
        Updates the UI component and its children.

        If any component in the tree returns True, the entire tree will be re-blitted.

        Returns
        -------
        bool
            Whether there is a component in the tree that wants to redraw itself.
        """
        dirty = False
        for child in self.__children:
            dirty = child.update(delta) or dirty
        if dirty:
            logging.debug(f"{self.name} returning dirty from update()")
        return dirty


    def build_static_blit_surface(self, dest: pygame.Surface, parent_pos: pygame.Vector2):
        """
        Recursively blit each static component in the tree to the given surface.
        """
        # _blit_surface can change a component's self._rect (e.g., Spinner), so we need to call _blit_surface on every
        # component as we walk the tree in order to compute each component's screen position. This is bad design;
        # as a property, _blit_surface shouldn't change state.
        bs = self._blit_surface
        topleft = pygame.Vector2(self._rect.topleft) + parent_pos
        if self._is_static:
            dest.blit(bs, topleft, special_flags = pygame.BLEND_ALPHA_SDL2)
        for child in self.__children:
            child.build_static_blit_surface(dest, topleft)


    def get_dynamic_blit_surfaces(self, parent_pos: pygame.Vector2 = pygame.Vector2()) -> list[BlitSurface]:
        """
        Walks the UI tree computing screen coordinates for each component and building a list of dynamic component
        blit surfaces and screen coordinates.

        A static component is one that doesn't need to change its blit surface on every frame. A dynamic component
        is one that needs its blit surface updated every frame.
        """
        bss = []
        # _blit_surface can change a component's self._rect (e.g., Spinner), so we need to call _blit_surface on every
        # component as we walk the tree in order to compute each component's screen position. This is bad design;
        # as a property, _blit_surface shouldn't change state.
        bs = self._blit_surface
        topleft = pygame.Vector2(self._rect.topleft) + parent_pos
        if not self._is_static:
            bss.append(BlitSurface(bs, topleft))
        for child in self.__children:
            bss.extend(child.get_dynamic_blit_surfaces(topleft))
        return bss


    def resize_to_parent(self, parent_rect: pygame.rect):
        """
        Resizes the component's rect to match size with its parent's rect.

        _rect is always in parent coordinates, NOT screen coordinates.
        """
        width = parent_rect.width * self.__size.x
        height = parent_rect.height * self.__size.y

        if self.__fix_aspect_ratio:
            if self.__aspect_ratio is None:
                self.__aspect_ratio = width / height
            if width / self.__aspect_ratio > height:
                # Height is the limiting factor
                width = self.__aspect_ratio * height
            elif height * self.__aspect_ratio > width:
                # Width is the limiting factor
                height = width / self.__aspect_ratio

        pos = pygame.Vector2(parent_rect.width * self._normalized_pos.x, parent_rect.height * self._normalized_pos.y)
        self._rect = pygame.Rect(pos.x, pos.y, width, height)
        self._parent_rect = parent_rect
        self._parent_rect_changed = True

        for child in self.__children:
            child.resize_to_parent(self._rect)


    def process_mouse_event(self, pos: pygame.Vector2, event_type: int) -> bool:
        """
        Gives the component and its children a mouse event to process.

        Parameters
        ----------
        pos
            Mouse position in parent coordinates.
        event
            A pygame input event type; one of pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION,
            pygame.MOUSEWHEEL.

        Returns
        -------
        bool
            Whether there was a component in the tree that did something with the information.
        """
        if not self._parent_rect:
            return False

        capture_event = False
        local_pos = pos - pygame.Vector2(self._parent_rect.topleft)
        for child in self.__children:
            capture_event = capture_event or child.process_mouse_event(local_pos, event_type)

        if not capture_event:
            # My kids weren't interested in the event. Am I interested?
            capture_event = event_type in self.__wanted_mouse_events and self._rect.collidepoint(local_pos)

        if event_type == pygame.MOUSEMOTION:
            if capture_event:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

        return capture_event


    @property
    def _is_static(self) -> bool:
        return True


    @property
    def name(self) -> str:
        return self.__name


    @property
    def rect(self) -> pygame.rect:
        return self._rect


    @property
    @abstractmethod
    def _blit_surface(self) -> pygame.Surface:
        """Returns the image that the UI component wants to blit to the screen."""
        pass


    def __iter__(self):
        return iter(self.__children)
