import pygame

from UI.panel import Panel
from class_registrar import ClassRegistrar


@ClassRegistrar.register("Spinner")
class Spinner(Panel):
    """UI component that spins the given image."""

    def __init__(self, angular_velocity, **kwargs):
        super().__init__(**kwargs)
        self.angular_velocity = angular_velocity
        self.angle = 0

    def resize(self):
        """Resizes the image to match the panel's size with its parent's rect."""
        scale = self.rect.width / self.image_asset.get_rect().width
        self.image = pygame.transform.rotozoom(self.image_asset, self.angle, scale)
        # Shift self.rect so that image spins around its centre point
        image_rect = self.image.get_rect()
        self.rect.x -= ((image_rect.width - self.rect.width) / 2)
        self.rect.y -= ((image_rect.height - self.rect.height) / 2)

    def update(self, parent_rect, delta):
        """Updates the UI component and its children."""
        super().update(parent_rect, delta)
        spin_delta = (self.angular_velocity * delta) / 1000.0
        self.angle = (self.angle + spin_delta) % 360

    def is_dirty(self):
        """This component is always dirty because it's spinning."""
        return True
