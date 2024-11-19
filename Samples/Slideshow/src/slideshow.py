import pygame
import pygamengn

from photo_spawner import PhotoSpawner


@pygamengn.ClassRegistrar.register("Slideshow")
class Slideshow(pygamengn.Game):

    def __init__(
            self,
            photo_spawner,
            slideshow_ui,
            photo_info_ui,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.running = True

        self.slideshow_ui = slideshow_ui
        self.photo_info_ui = photo_info_ui
        self.show_ui(self.slideshow_ui, 500)

        self.photo_spawner = photo_spawner
        self.photo_spawner.set_slideshow_ui(slideshow_ui)
        self.photo_spawner.set_info_ui(photo_info_ui)
        self.photo_spawner.move_to_next_photo()
        self.is_paused = False

    def update(self, delta):
        """Updates the game."""
        self.handle_input()

        if not self.is_paused:
            self.photo_spawner.update(delta)

            if self.photo_spawner.done:
                self.running = False

        super().update(delta)

    def handle_input(self):
        """Reads input and makes things happen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.photo_spawner.move_to_next_photo()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.photo_spawner.move_to_prev_photo()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.photo_spawner.show_info_ui = self.toggle_ui(self.photo_info_ui, 200)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_paused = not self.is_paused
