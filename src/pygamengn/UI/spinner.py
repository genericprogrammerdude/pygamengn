import logging

import pygame

from pygamengn.UI.component import Component
from pygamengn.UI.panel import TexturePanel
from pygamengn.class_registrar import ClassRegistrar



@ClassRegistrar.register("Spinner")
class Spinner(TexturePanel):
    """UI component that spins its texture image at an angular velocity expressed in degrees per second."""

    def __init__(self, angular_velocity = 0, **kwargs):
        super().__init__(**kwargs)
        self.__angular_velocity = angular_velocity
        self.__angle = 0

    def update(self, parent_rect: pygame.rect, delta: int, animators: list[Component]) -> bool:
        """Updates the UI component and its children."""
        rv = super().update(parent_rect, delta, animators)
        spin_delta = (self.__angular_velocity * delta) / 1000
        self.__angle = (self.__angle + spin_delta) % 360
        animators.append(self)
        return False

    @property
    def _blit_surface(self) -> pygame.Surface:
        """Returns the image that the UI component wants to blit to the screen."""
        scale = self.rect.width / self._image_asset.get_rect().width
        self._image = pygame.transform.rotozoom(self._image_asset, self.__angle, scale)
        # Shift self._rect so that image spins around its centre point
        image_rect = self._image.get_rect()
        self._resize_to_parent(self._parent_rect)
        self._rect.x -= ((image_rect.width - self._rect.width) / 2)
        self._rect.y -= ((image_rect.height - self._rect.height) / 2)
        return super()._blit_surface

    def _parent_rect_changed(self):
        # Need to override this because Panel deletes self._image and Spinner recomputes its self._rect every frame.
        pass
