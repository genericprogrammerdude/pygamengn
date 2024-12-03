import random

import pygame

from pygamengn.atlas import Atlas
from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject


@ClassRegistrar.register("AnimatedTexture")
class AnimatedTexture(GameObject):

    def __init__(self, atlas, duration, sound=None, **kwargs):
        super().__init__(atlas.frames[0][0], False, **kwargs)
        self.dirty_image = False
        self.atlas = atlas
        self.duration = duration
        self.sound = sound
        self.animation_time = 0
        self.is_playing = False
        self.atlas_index = 0

    def update(self, delta):
        super().update(delta)

        if self.is_playing:
            # Figure out which frame to use and set the image
            progress = 1.0 * self.animation_time / self.duration
            frames = self.atlas.frames[self.atlas_index]
            frame_index = round(progress * len(frames))
            if frame_index < len(frames):
                self.image = frames[frame_index]
                self.rect = self.image.get_rect()

            self.rect = self.image.get_rect()
            self.rect.x = self.position[0] - round(self.image.get_rect().width / 2)
            self.rect.y = self.position[1] - round(self.image.get_rect().height / 2)

            # Update animation time
            self.animation_time = self.animation_time + delta
            if self.animation_time > self.duration:
                if self.done_callback:
                    self.done_callback()
                self.reset()

    def play(self, done_callback=None):
        self.is_playing = True
        self.atlas_index = random.randint(0, len(self.atlas.frames) - 1)
        self.done_callback = done_callback
        if self.sound:
            self.sound.play()

    def reset(self):
        """Resets the animation and leaves the object ready to play from the start."""
        self.animation_time = 0
        self.is_playing = False
        self.done_callback = None
        self.kill()

    def take_damage(self, *_):
        pass
