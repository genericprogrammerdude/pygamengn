from abc import abstractmethod

import logging
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase



@ClassRegistrar.register("UIBase")
class UIBase(GameObjectBase):
    """
    Base class for UI components.

    This class takes care of administrative and basic geometric issues. Its functionality is limited to the following
    topics by design:
        1. Keep its own geometry updated to the geometry of its parent rectangle.
        2. Manage addition and removal of children.
        3. Keep children's geometry updated to any changes to its own geometry.

    In addition, this class must always be instantiable as a parent container of other UI components that need to be
    kept together under a single parent.
    """

    def __init__(self, pos, size, children, fix_aspect_ratio, name="", wanted_mouse_events = list[int], **kwargs):
        super().__init__(**kwargs)
        self.__size = pygame.Vector2(size)
        self.__children = children
        self.__fix_aspect_ratio = fix_aspect_ratio
        self.__name = name
        self.__wanted_mouse_events = wanted_mouse_events
        self.__aspect_ratio = None

        self.__bind_children()

        self._normalized_pos = pygame.Vector2(pos)
        self._parent_rect = None
        self._rect = None


    def update(self, parent_rect: pygame.rect, delta: int):
        """Updates the UI component and its children."""
        if not self._parent_rect or parent_rect.size != self._parent_rect.size:
            # If my parent_rect changed, I need to resize and so do my children
            self.__resize_to_parent(parent_rect)

        for child in self.__children:
            child.update(self._rect, delta)


    @abstractmethod
    def draw(self, image: pygame.Surface = None):
        for child in self.__children:
            child.draw(image)


    ### ACHTUNG!
    ### This is temporary! It should not be needed!
    @property
    def children(self) -> list:
        return self.__children


    ### ACHTUNG!
    ### This is temporary! It should not be needed!
    @property
    def rect(self) -> pygame.rect:
        return self._rect


    @property
    def parent_rect(self) -> pygame.rect:
        return self._parent_rect


    # @parent_rect.setter
    # def parent_rect(self, pygame.rect):
    #     if parent_rect.size != self._parent_rect.size:
    #         # If my parent_rect changed, I need to resize and so do my children
    #         self.__resize_to_parent(parent_rect)
    #         for child in self.__children:
    #             child.__resize_to_parent(self._parent_rect)


    def __resize_to_parent(self, parent_rect):
        """Resizes the component's rect to match size with its parent's rect."""
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
        # self._rect is always in parent coordinates, NOT screen coordinates
        self._rect = pygame.Rect(pos.x, pos.y, width, height)
        self._parent_rect = parent_rect


    # def propagate_mouse_pos(self, pos: pygame.Vector2) -> bool:
    #     """
    #     Tells the component and its children the position of the mouse pointer in screen coordinates.

    #     Parameters
    #     ----------
    #     pos
    #         Mouse position in screen coordinates.

    #     Returns
    #     -------
    #     bool
    #         Whether there was a component in the tree that did something with the information.
    #     """
    #     i = 0
    #     capture_hover = False
    #     while not capture_hover and i < len(self.__children):
    #         capture_hover = self.__children[i].propagate_mouse_pos(pos - pygame.Vector2(self._parent_rect.topleft))
    #         i += 1

    #     if capture_hover:
    #         pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
    #     else:
    #         pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
    #     return capture_hover


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


    def __bind_children(self, parent=None):
        """Binds children to class members to make them accessible."""
        if not parent:
            parent = self
        for child in self.__children:
            child.__bind_children(parent)
            if child.name:
                try:
                    a = getattr(parent, child.name)
                    logging.warn(f"{child.name} attr is already assigned with {child}. Not assigning it {a}")
                except AttributeError:
                    setattr(parent, child.name, child)


    def _is_mouse_event(self, event_type: int) -> bool:
        return (
            event_type == pygame.MOUSEBUTTONDOWN or
            event_type == pygame.MOUSEBUTTONUP or
            event_type == pygame.MOUSEMOTION or
            event_type == pygame.MOUSEWHEEL
        )


    @property
    def name(self):
        return self.__name
