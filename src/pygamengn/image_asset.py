from __future__ import annotations

import logging

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase



@ClassRegistrar.register("ImageAsset")
class ImageAsset(GameObjectBase):
    """Loadable image asset."""

    def __init__(
        self,
        fname: str,
        scale: float = 1.0,
        alpha: float = 1.0,
        angle: int = 0,
        cache_rotations: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.__fname = fname
        self.__base_surface = pygame.transform.rotozoom(pygame.image.load(self.__fname), angle, scale)
        self.__alpha = alpha
        if self.__alpha != 1.0:
            tmp = pygame.Surface(self.__base_surface.get_rect().size, pygame.SRCALPHA)
            tmp.fill((255, 255, 255, self.__alpha * 255))
            self.__base_surface.blit(tmp, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)
        self.__cache_rotations = cache_rotations
        self.__scaled_rotations = {}
        if self.__cache_rotations:
            self.__scaled_rotations[1.0] = [
                pygame.transform.rotozoom(self.__base_surface, i, 1.0) for i in range(0, 360)
            ]
        else:
            self.__scaled_rotations[1.0] = [self.__base_surface]


    @property
    def surface(self) -> pygame.Surface:
        """Returns the image with 0-degree rotation and scale of 1."""
        return self.__base_surface


    def get_surface(self, rotation: float = 0.0, scale: float = 1.0, force_cache: bool = False):
        """Returns the image at the given rotation and scale."""
        try:
            return self.__scaled_rotations[scale][round(rotation)]

        except KeyError:
            rv = None
            logging.warn(f"ImageAsset '{self.__fname}': Scale {scale} is not cached.")
            if force_cache:
                logging.warn(f"ImageAsset '{self.__fname}': Force-caching scale {scale}.")
                self.cache_scale(scale)
                rv = self.__scaled_rotations[scale][rotation]
            return rv

        except IndexError:
            logging.debug(f"ImageAsset '{self.__fname}': Rotation angle {rotation} is not cached. Rotating base surface.")
            return pygame.transform.rotozoom(self.__scaled_rotations[scale][0], rotation, scale)


    def cache_scale(self, scale: float):
        """Caches the image at the given scale."""
        if not scale in self.__scaled_rotations:
            if self.__cache_rotations:
                self.__scaled_rotations[scale] = [
                    pygame.transform.rotozoom(self.__base_surface, i, scale) for i in range(360)
                ]
            else:
                self.__scaled_rotations[scale] = [pygame.transform.smoothscale_by(self.__base_surface, scale)]
        else:
            logging.warn(f"ImageAsset '{self.__fname}': Scale {scale} is already cached.")
