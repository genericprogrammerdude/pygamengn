import logging

import pygame

from pygamengn.UI.panel import TexturePanel
from pygamengn.class_registrar import ClassRegistrar



@ClassRegistrar.register("Spinner")
class Spinner(TexturePanel):
    """UI component that spins its texture image at an angular velocity expressed in degrees per second."""

    def __init__(self, angular_velocity = 0, **kwargs):
        super().__init__(**kwargs)
        self.__angular_velocity = angular_velocity
        self.__angle = 0

    def update(self, delta: int) -> bool:
        """Updates the UI component and its children."""
        spin_delta = (self.__angular_velocity * delta) / 1000
        self.__angle = (self.__angle + spin_delta) % 360
        rv = super().update(delta)
        return False

    def _draw_surface(self):
        scale = self.rect.width / self._image_asset.get_rect().width
        self._surface = pygame.transform.rotozoom(self._image_asset, self.__angle, scale)
        # Shift self._rect so that image spins around its centre point
        surface_rect = self._surface.get_rect()
        self.resize_to_parent(self._parent_rect)
        self._rect.x -= ((surface_rect.width - self._rect.width) / 2)
        self._rect.y -= ((surface_rect.height - self._rect.height) / 2)

    @property
    def _needs_redraw(self) -> bool:
        """Spinner redraws its surface on every frame."""
        return True

    @property
    def _is_dynamic(self) -> bool:
        """Spinner is a dynamic component (it needs to redraw and reblit on every update)."""
        return True
