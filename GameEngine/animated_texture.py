import pygame

from game_object import GameObject


class AnimatedTexture(GameObject):

    def __init__(self, image_fname, frame_size, duration):
        super().__init__(image_fname, False)
        self.frame_size = frame_size
        self.duration = duration
        self.animation_time = 0
        self.is_playing = False

        # Build frame images from atlas
        self.frames = []
        for y in range(0, self.rect.height, frame_size[1]):
            for x in range(0, self.rect.width, frame_size[0]):
                rect = pygame.Rect(x, y, frame_size[0], frame_size[1])
                frame = self.image.subsurface(rect)
                self.frames.append(frame)
        self.image = self.frames[0]

    def update(self, delta):
        super().update(delta)

        if self.is_playing:
            # Figure out which frame to use and set the image
            progress = 1.0 * self.animation_time / self.duration
            frame_index = round(progress * len(self.frames))
            if frame_index < len(self.frames):
                self.image = self.frames[frame_index]

            self.rect = self.image.get_rect()

            # Update animation time
            self.animation_time = self.animation_time + delta
            if self.animation_time > self.duration:
                self.reset()

    def play(self):
        self.is_playing = True

    def reset(self):
        """Resets the animation and leaves the object ready to play from the start."""
        self.animation_time = 0
        self.is_playing = False
        self.kill()
