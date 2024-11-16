import logging
import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase
from pygamengn.interpolator import Interpolator
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
        self._fade_interp = None
        self._fade_duration = 0


    def update(self, parent_rect: pygame.rect, delta: int) -> bool:
        """
        Updates the UI component and its children.

        Returns a bool indicating whether the UI wants to continue participating in Game's update loop.
        """
        keep_updating = True
        self._is_dirty = self._component.update(parent_rect, delta)
        if self._fade_interp:
            if self._fade_interp.duration > self._fade_duration:
                self._fade_duration += delta
            else:
                if self._fade_interp.to_value == 0:
                    keep_updating = False
                self._fade_interp = None
                self._fade_duration = 0
        return keep_updating


    def blit_to_surface(self, surface: pygame.Surface):
        """Blits the root image that represents this entire UI tree to the given surface."""
        if self._is_dirty:
            self._root_blit_image = pygame.Surface(self._component.rect.size, pygame.SRCALPHA)
            self._component.build_blit_image(self._root_blit_image, -pygame.Vector2(self._component.rect.topleft))
        if self._fade_interp:
            self._root_blit_image.set_alpha(self._fade_interp.get(self._fade_duration))
        surface.blit(
            source = self._root_blit_image,
            dest = self._component.rect.topleft,
            special_flags = pygame.BLEND_ALPHA_SDL2
        )


    def fade_in(self, duration: int):
        self._fade(0, 255, duration)


    def fade_out(self, duration: int):
        """Fades teh UI out. After the specified duration the UI will ask to be removed from the update loop."""
        self._fade(255, 0, duration)


    def _fade(self, from_alpha: int, to_alpha: int, duration: int):
        """Fades the UI from/to the specified alpha values in the specified duration."""
        if self._fade_interp:
            from_alpha = self._fade_interp.get(self._fade_duration)
        self._fade_interp = Interpolator(duration, from_alpha, to_alpha)
        self._fade_duration = 0

    def _bind_children(self):
        """Binds component and its children to data members of this Root; only Components that have a name are bound."""
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
