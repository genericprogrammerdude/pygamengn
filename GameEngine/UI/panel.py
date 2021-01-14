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


@GameObjectFactory.register("ColourPanel")
class ColourPanel(UIBase):
    """Basic UI panel that is a solid colour and has no image."""

    def __init__(self, colour, **kwargs):
        super().__init__(**kwargs)
        self.colour = colour

    def resize(self):
        """Resizes the image to match the panel's size with its parent's rect."""
        self.image = pygame.Surface(self.rect.size, pygame.HWSURFACE | pygame.SRCALPHA)
        self.image.fill(self.colour)


@GameObjectFactory.register("TextPanel")
class TextPanel(UIBase):
    """Panel that sets its size to the size of the text in it. This panel ignores the parent rect."""

    def __init__(self, font_asset, text_colour, text, **kwargs):
        super().__init__(**kwargs)
        self.font_asset = font_asset
        self.text_colour = text_colour
        self.text = text
        self.text_is_dirty = True
        self.fix_aspect_ratio = True

    def set_text(self, text):
        self.text_is_dirty = (self.text != text)
        self.text = text

    def is_dirty(self):
        return self.text_is_dirty

    def resize(self):
        """TextPanel ignores its parent rect and renders to the font size."""
        self.image = self.font_asset.font.render(self.text, True, self.text_colour)
        pos = self.rect.topleft
        image_rect = self.image.get_rect()
        self.rect = pygame.Rect(pos[0], pos[1], image_rect.width, image_rect.height)
        self.text_is_dirty = False
