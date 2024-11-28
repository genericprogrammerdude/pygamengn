import logging

import pygame

from pygamengn.UI.texture_panel import TexturePanel
from pygamengn.class_registrar import ClassRegistrar



@ClassRegistrar.register("Spinner")
class Spinner(TexturePanel):
    """UI component that spins its texture image at an angular velocity expressed in degrees per second."""

    def __init__(self, angular_velocity = 0, **kwargs):
        super().__init__(**kwargs)
        self._angular_velocity = angular_velocity

    def update(self, delta: int) -> bool:
        """Updates the UI component and its children."""
        if self._angular_velocity != 0:
            spin_delta = (self._angular_velocity * delta) / 1000
            self.angle = (self._angle + spin_delta) % 360
        rv = super().update(delta)
        return False if self._is_dynamic else rv

    @property
    def _is_dynamic(self) -> bool:
        """
        Spinner is a dynamic component if its angular velocity is not 0.
        A dynamic component needs to redraw and reblit on every update.
        """
        return self._angular_velocity != 0
