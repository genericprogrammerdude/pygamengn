from enum import Enum, auto
import random

import pygame
import pygamengn

from photo import PhotoSpawner


@pygamengn.ClassRegistrar.register("Slideshow")
class Slideshow(pygamengn.Game):

    def __init__(
            self,
            photo_spawner,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.running = True
        self.photo_spawner = photo_spawner

    def update(self, delta):
        """Updates the game."""
        self.handle_input()
        self.photo_spawner.update(delta)
        super().update(delta)

        self.running = not self.photo_spawner.done or len(self.render_group.sprites()) > 0

    def handle_input(self):
        """Reads input and makes things happen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
