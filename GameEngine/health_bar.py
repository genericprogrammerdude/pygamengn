import pygame

from game_object import GameObject
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("HealthBar")
class HealthBar(GameObject):

    def __init__(self, images, **kwargs):
        super().__init__(images[0], **kwargs)
        self.images = images

    def update(self, delta):
        self.dirty_image = False
        if self.parent:
            bg = self.images[0].copy()
            fg = self.images[1].copy()
            scale = self.parent.health / 100.0
            size = bg.get_rect().size
            fg = pygame.transform.scale(fg, (size[0], round(scale * size[1])))
            bg.blit(fg, (0, 0))
            self.image = pygame.transform.rotate(bg, self.heading)
            self.rect = self.image.get_rect()
            self.pos = self.parent.pos + pygame.Vector2(0.0, self.parent.rect.height * 0.75)
        super().update(delta)
