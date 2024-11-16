import logging
import pygame

from pygamengn.blit_surface import BlitSurface
from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase
from pygamengn.UI.component import Component



@ClassRegistrar.register("Root")
class Root(GameObjectBase):
    """
    This class is the only UI class that Game knows and deals with; it provides a simple interface for Game to use.
    Every UI screen with UI components should inherit from Root.
    """

    def __init__(self, component: Component, **kwargs):
        super().__init__(**kwargs)
        self._component = component
        self._bind_children()
        self._root_blit_image = None
        self._is_dirty = True


    def update(self, parent_rect: pygame.rect, delta: int):
        """
        Updates the UI component and its children.
        """
        self._is_dirty = self._component.update(parent_rect, delta)


    @property
    def root_blit_surface(self) -> BlitSurface:
        """Returns the root image that represents this entire UI tree."""
        if self._is_dirty:
            self._root_blit_image = pygame.Surface(self._component.rect.size, pygame.SRCALPHA)
            self._component.build_blit_image(self._root_blit_image, -pygame.Vector2(self._component.rect.topleft))
        return BlitSurface(surface = self._root_blit_image, topleft = self._component.rect.topleft)


    def _bind_children(self):
        """Binds component and its children to data members of this Root."""
        stack = [self._component]
        while len(stack) > 0:
            component = stack.pop()
            if component.name:
                try:
                    a = getattr(self, component.name)
                    logging.warn(f"{component.name} attr is already assigned with {a}. Not assigning it {component}")
                except AttributeError:
                    setattr(self, component.name, component)
            for child in component:
                stack.append(child)
