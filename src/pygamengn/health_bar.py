import pygame

from pygamengn.blit_surface import BlitSurface
from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject


@ClassRegistrar.register("HealthBar")
class HealthBar(GameObject):

    def __init__(self, bg_image_asset, fg_image_asset, **kwargs):
        super().__init__(None, **kwargs)
        self.__background = bg_image_asset.surface
        self.__foreground = fg_image_asset.surface
        self.__fg_asset = fg_image_asset
        self.rect = self.__background.get_rect()

    def update(self, delta):
        self._dirty_image = False
        if self.parent:
            scale = self.parent.health / 100.0
            size = self.__background.get_rect().size
            self.__foreground = pygame.transform.scale(self.__fg_asset.surface, (round(scale * size[0]), size[1]))
            self.position = self.parent.position + pygame.Vector2(0.0, self.parent.rect.height * 0.75)
        super().update(delta)

    @property
    def blit_surfaces(self) -> list[BlitSurface]:
        return [BlitSurface(self.__background, self.rect), BlitSurface(self.__foreground, self.rect)]
