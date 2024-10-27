from enum import Enum, auto
import random

import pygame
import pygamengn


@pygamengn.ClassRegistrar.register("Slideshow")
class Slideshow(pygamengn.Game):

    def __init__(
            self,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.running = True

    def update(self, delta):
        """Updates the game."""

        self.handle_input()

        super().update(delta)

    def handle_input(self):
        """Reads input and makes things happen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
