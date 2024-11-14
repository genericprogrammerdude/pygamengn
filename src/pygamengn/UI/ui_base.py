from abc import ABCMeta, abstractmethod

import logging
import pygame

from pygamengn.blit_surface import BlitSurface
from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase



@ClassRegistrar.register("UIBase")
class UIBase(GameObjectBase, metaclass = ABCMeta):
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


    def __init__(
        self,
        pos,
        size,
        children,
        fix_aspect_ratio,
        is_ui_root = False,
        name="",
        wanted_mouse_events = list[int],
        **kwargs
    ):
        super().__init__(**kwargs)
        self.__size = pygame.Vector2(size)
        self.__children = children
        self.__fix_aspect_ratio = fix_aspect_ratio
        self.__is_ui_root = is_ui_root
        self.__name = name
        self.__wanted_mouse_events = wanted_mouse_events
        self.__aspect_ratio = None

        if self.__is_ui_root:
            self.__bind_children()
            self.__root_blit_image = None
            self.__root_is_dirty = True

        self._normalized_pos = pygame.Vector2(pos)
        self._parent_rect = None
        self._rect = None


    def update(self, parent_rect: pygame.rect, delta: int) -> bool:
        """
        Updates the UI component and its children.

        Returns
        -------
        bool
            Whether there is a component in the tree that wants to redraw itself.
        """
        dirty = False
        if not self._parent_rect or parent_rect.size != self._parent_rect.size:
            # If my parent_rect changed, I need to resize and so do my children
            self.__resize_to_parent(parent_rect)
            self._draw()
            dirty = True

        for child in self.__children:
            dirty = child.update(self._rect, delta) or dirty

        # Now that everyone has had a chance to update, the root UI needs to produce an image
        if self.__is_ui_root:
            self.__root_is_dirty = dirty

        return dirty


    def __build_blit_image(self, screen_image: pygame.Surface, parent_pos: pygame.Vector2):
        """
        Recursively builds the image to be blit to the screen. This image will have the images for all the components
        in the UI tree.
        """
        bs = self._blit_surface
        topleft = pygame.Vector2(self._rect.topleft) + parent_pos
        if bs:
            draw_rect = screen_image.blit(bs, topleft, special_flags = pygame.BLEND_ALPHA_SDL2)
            print(f"{self.__name}: {draw_rect.topleft} {draw_rect.size}")
        for child in self.__children:
            child.__build_blit_image(screen_image, topleft)


    @property
    def root_blit_surface(self) -> BlitSurface:
        """Returns the root image onto the destination surface. This only works for the root UI."""
        if self.__is_ui_root:
            if self.__root_is_dirty:
                self.__root_blit_image = pygame.Surface(self._rect.size, pygame.SRCALPHA)
                self.__build_blit_image(self.__root_blit_image, -pygame.Vector2(self._rect.topleft))
                self.__root_is_dirty = False
            return BlitSurface(surface = self.__root_blit_image, topleft = self._rect.topleft)
        else:
            logging.warn(
                f"Calling UIBase.blit_root_surface() on a UIBase instance that is not UI root ({self.__name}.__is_ui_root == False)"
            )
            return None


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
        print(f"{self.__name}: _rect{self._rect}, _parent_rect{self._parent_rect}")


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


    @property
    def name(self):
        return self.__name


    @property
    @abstractmethod
    def _blit_surface(self) -> pygame.Surface:
        """Returns the image that the UI component wants to blit to the screen."""
        pass


    @abstractmethod
    def _draw(self):
        """
        Draws the image that represents this UIBase. Each UIBase subclass is responsible for deciding whether it needs
        to produce a new image or use a previously existing one.
        The UI root will call this method if the component returns True from its update().
        """
        pass
