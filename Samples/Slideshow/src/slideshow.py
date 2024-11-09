import pygame
import pygamengn

from photo_spawner import PhotoSpawner


@pygamengn.ClassRegistrar.register("Slideshow")
class Slideshow(pygamengn.Game):

    def __init__(
            self,
            photo_spawner,
            year_panel,
            photo_info_panel,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.running = True
        self.year_panel = year_panel
        self.photo_info_panel = photo_info_panel
        self.photo_spawner = photo_spawner
        self.photo_spawner.set_year_panel(year_panel)
        self.photo_spawner.move_to_next_photo()

    def update(self, delta):
        """Updates the game."""
        self.handle_input()
        self.year_panel.update(self.screen.get_rect(), delta)
        self.photo_info_panel.update(self.screen.get_rect(), delta)
        self.photo_spawner.update(delta)
        self.blit_ui(self.year_panel)
        self.blit_ui(self.photo_info_panel)
        super().update(delta)

        if self.photo_spawner.done:
            self.running = False

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
