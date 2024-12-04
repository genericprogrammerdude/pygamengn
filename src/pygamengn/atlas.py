import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase


@ClassRegistrar.register("Atlas")
class Atlas(GameObjectBase):
    """Texture atlas that can be shared by GameObjects."""

    def __init__(self, frame_size, images, scale = 1):
        # Build frame images from atlas
        self.frame_size = frame_size
        self.images = images
        self.frames = []
        for img in self.images:
            rect = img.get_rect()
            image_frames = []
            frame_index = 0
            for y in range(0, rect.height, frame_size[1]):
                for x in range(0, rect.width, frame_size[0]):
                    frame_rect = pygame.Rect(x, y, frame_size[0], frame_size[1])
                    image_frames.append(
                        pygame.transform.smoothscale_by(img.subsurface(frame_rect), scale)
                    )
            self.frames.append(image_frames)
