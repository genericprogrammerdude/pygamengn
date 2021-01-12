import pygame

from UI.ui_base import UIBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Panel")
class Panel(UIBase):
    """Basic UI panel that shows an image."""

    def __init__(self, image_asset, **kwargs):
        super().__init__(**kwargs)
        self.image_asset = image_asset
        rect = image_asset.get_rect()
        self.aspect_ratio = rect.width / rect.height

    def resize(self):
        """Resizes the image to match the panel's size with its parent's rect."""
        self.image = pygame.transform.scale(self.image_asset, self.rect.size)


@GameObjectFactory.register("PanelColour")
class PanelColour(UIBase):
    """Basic UI panel that is a solid colour and has no image."""

    def __init__(self, colour, **kwargs):
        super().__init__(**kwargs)
        self.colour = colour

    def resize(self):
        """Resizes the image to match the panel's size with its parent's rect."""
        self.image = pygame.Surface(self.rect.size, pygame.HWSURFACE | pygame.SRCALPHA)
        self.image.fill(self.colour)
