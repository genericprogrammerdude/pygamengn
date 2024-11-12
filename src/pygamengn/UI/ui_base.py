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

    def __init__(self, pos, size, children, fix_aspect_ratio, name="", **kwargs):
        super().__init__(**kwargs)
        self.__normalized_pos = pygame.Vector2(pos)
        self.__size = pygame.Vector2(size)
        self.__children = children
        self.__fix_aspect_ratio = fix_aspect_ratio
        self.__name = name
        self.__aspect_ratio = None
        self.__is_dirty = True

        self.__bind_children()

        self._parent_rect = None
        self._rect = None


    def update(self, parent_rect: pygame.rect, delta: int):
        """Updates the UI component and its children."""
        if self.__is_dirty or parent_rect.size != self._parent_rect.size:
            self.__resize_to_parent(parent_rect)
            self.__is_dirty = False

        for child in self.__children:
            child.update(self._rect, delta)


    ### ACHTUNG!
    ### This is temporary! It should not be needed!
    @property
    def children(self) -> list:
        return self.__children


    @property
    def rect(self) -> pygame.rect:
        return self._rect


    @property
    def normalized_pos(self) -> pygame.Vector2:
        return self.__normalized_pos


    # @normalized_pos.setter
    # def normalized_pos(self, normalized_pos: pygame.Vector2):
    #     """Sets the normalized position of the UI base. Both dimensions are must be in the range [0, 1]."""
    #     if normalized_pos.x < 0 or normalized_pos.x > 1 or normalized_pos.y < 0 or normalized_pos.y:
    #         raise ValueError("Both dimensions of a normalized position must be in the range [0, 1]")

    #     if self.__normalized_pos != normalized_pos:
    #         self.__is_dirty = True
    #         self.__normalized_pos = normalized_pos
    #         for child in self.__children:
    #             child.__is_dirty = True


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
        pos = parent_rect.topleft + pygame.Vector2(
            parent_rect.width * self.__normalized_pos.x, parent_rect.height * self.__normalized_pos.y
        )
        self._rect = pygame.Rect(pos.x, pos.y, width, height)
        self._parent_rect = parent_rect
        self.__is_dirty = False


    def propagate_mouse_pos(self, pos) -> bool:
        """
        Tells the component and its children the position of the mouse pointer in screen coordinates.

        Returns
        -------
        bool
            Whether there was a component in the tree that did something with the information.
        """
        i = 0
        capture_hover = False
        while not capture_hover and i < len(self.__children):
            capture_hover = self.__children[i].propagate_mouse_pos(pos)
            i += 1

        if capture_hover:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return capture_hover


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
