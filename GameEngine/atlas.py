import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Atlas")
class Atlas(GameObjectBase):
    """Texture atlas that can be shared by GameObjects."""

    def __init__(self, frame_size, images):
        # Build frame images from atlas
        self.frame_size = frame_size
        self.images = images
        self.frames = []
        for img in self.images:
            rect = img.get_rect()
            image_frames = []
            for y in range(0, rect.height, frame_size[1]):
                for x in range(0, rect.width, frame_size[0]):
                    frame_rect = pygame.Rect(x, y, frame_size[0], frame_size[1])
                    frame = img.subsurface(frame_rect)
                    image_frames.append(frame)
            self.frames.append(image_frames)
