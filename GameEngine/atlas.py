import pygame


class Atlas():
    """Texture atlas that can be shared by GameObjects."""

    def __init__(self, image, frame_size):
        # Build frame images from atlas
        rect = image.get_rect()
        self.frame_size = frame_size
        self.frames = []
        for y in range(0, rect.height, frame_size[1]):
            for x in range(0, rect.width, frame_size[0]):
                rect = pygame.Rect(x, y, frame_size[0], frame_size[1])
                frame = image.subsurface(rect)
                self.frames.append(frame)
