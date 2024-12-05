from __future__ import annotations
from abc import abstractmethod

import logging
import pygame

from pygamengn.blit_surface import BlitSurface
from pygamengn.class_registrar import ClassRegistrar
from pygamengn.console_registrar import ConsoleRegistrar
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

    debug_draw_ui_borders = False

    @classmethod
    def toggle_ui_borders(cls):
        Component.debug_draw_ui_borders = not Component.debug_draw_ui_borders


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
        self._rect = None
        self._active = True


    def update(self, delta: int) -> bool:
        """
        Updates the UI component and its children.

        If any component in the tree returns True, the entire tree will be re-blitted.

        Returns
        -------
        bool
            Whether there is a component in the tree that wants to redraw itself.
        """
        if not self._active:
            return False

        dirty = False
        for child in self.__children:
            if child._active:
                dirty = child.update(delta) or dirty
        return dirty


    def build_static_blit_surface(self, dest: pygame.Surface, parent_pos: pygame.Vector2):
        """
        Recursively blit each static component in the tree to the given surface.
        """
        if not self._active:
            return

        topleft = pygame.Vector2(self._rect.topleft) + parent_pos
        if not self._is_dynamic:
            bs = self._blit_surface
            if bs:
                dest.blit(bs, topleft, special_flags = pygame.BLEND_ALPHA_SDL2)
                if Component.debug_draw_ui_borders:
                    pygame.draw.rect(dest, (0, 255, 255, 255), pygame.Rect(topleft, self._rect.size), width = 1)
        for child in self.__children:
            child.build_static_blit_surface(dest, topleft)


    def get_dynamic_blit_surfaces(self, parent_pos: pygame.Vector2 = pygame.Vector2()) -> list[BlitSurface]:
        """
        Walks the UI tree computing screen coordinates for each component and building a list of dynamic component
        blit surfaces and screen coordinates.

        A static component is one that doesn't need to change its blit surface on every frame. A dynamic component
        is one that needs its blit surface updated every frame.
        """
        if not self._active:
            return []

        bss = []
        topleft = pygame.Vector2(self._rect.topleft) + parent_pos
        if self._is_dynamic:
            bs = self._blit_surface
            if bs:
                bss.append(BlitSurface(bs, topleft))

        [bss.extend(child.get_dynamic_blit_surfaces(topleft)) for child in self.__children]

        return bss


    def resize_to_parent(self, parent_rect: pygame.Rect):
        """
        Resizes the component's rect to match size with its parent's rect.

        This method should be called on resize even when the Component is not active.

        _rect is always in parent coordinates, NOT screen coordinates.
        """
        if self._parent_rect == parent_rect:
            logging.debug(f"{self.name}: _parent_rect{self._parent_rect} == parent_rect{parent_rect}")
            return

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

        # Give subclasses a chance to adjust their rectangle before resizing their kids
        self._adjust_rect()

        [child.resize_to_parent(self._rect) for child in self.__children]


    def _adjust_rect(self):
        """
        Hook to allow subclasses to adjust their self._rect before their children's.

        Subclasses avoid implementing resize_to_parent() and use _adjust_rect() instead.
        """
        pass


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
        if not self._active:
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
    def normalized_size(self) -> pygame.Vector2:
        return self.__size


    @property
    def _is_dynamic(self) -> bool:
        """
        Returns whether the component is dynamic, meaning that it needs to redraw and reblit on every frame.

        Most components are considered dynamic and will update their surface infrequently and due to factors like
        window resizes. Some components will redraw and reblit on every update (e.g., if they're running some kind of
        animation). Those components are considered dynamic and are blitted to the root surface (typically the screen)
        separately from the static components (see Root.blit_to_surface()).
        """
        return False


    @property
    def name(self) -> str:
        return self.__name


    @property
    def rect(self) -> pygame.Rect:
        return self._rect


    @property
    def _blit_surface(self) -> pygame.Surface:
        """Returns the image that the UI component wants to blit to the screen."""
        return None


    @property
    def active(self) -> bool:
        """Returns whether the component is active. Inactive components's update() method is not invoked."""
        return self._active


    @active.setter
    def active(self, state: bool):
        self._active = state


    def __iter__(self):
        return iter(self.__children)


    def delete_child(self, child: Component) -> bool:
        """Deletes the given child component from this component's tree."""
        i = 0
        rv = False
        while i < len(self.__children):
            if child == self.__children[i]:
                self.__children.pop(i)
                rv = True
            else:
                rv = self.__children[i].delete_child(child) or rv
                i += 1
        return rv


ConsoleRegistrar.register("uiborders", Component.toggle_ui_borders)
