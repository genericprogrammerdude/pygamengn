import pygame

from atlas import Atlas
from game_object import GameObject
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("AnimatedTexture")
class AnimatedTexture(GameObject):

    def __init__(self, atlas, duration):
        super().__init__(atlas.frames[0], False)
        self.atlas = atlas
        self.duration = duration
        self.animation_time = 0
        self.is_playing = False
        self.image = self.atlas.frames[0]
        self.rect = self.image.get_rect()

    def update(self, delta):
        super().update(delta)

        if self.is_playing:
            # Figure out which frame to use and set the image
            progress = 1.0 * self.animation_time / self.duration
            frame_index = round(progress * len(self.atlas.frames))
            if frame_index < len(self.atlas.frames):
                self.image = self.atlas.frames[frame_index]
                if self.scale != 1:
                    self.image = pygame.transform.scale(self.image,
                                                        (self.image.get_rect().width * self.scale,
                                                        self.image.get_rect().height * self.scale))
                    print("WARNING! Scaling atlas frames!")
                self.rect = self.image.get_rect()

            self.rect = self.image.get_rect()
            self.rect.x = self.pos[0] - round(self.image.get_rect().width / 2)
            self.rect.y = self.pos[1] - round(self.image.get_rect().height / 2)

            # Update animation time
            self.animation_time = self.animation_time + delta
            if self.animation_time > self.duration:
                self.reset()
                self.kill()

    def play(self):
        self.is_playing = True

    def reset(self):
        """Resets the animation and leaves the object ready to play from the start."""
        self.animation_time = 0
        self.is_playing = False
        self.kill()
