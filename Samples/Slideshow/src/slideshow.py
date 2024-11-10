import pygame
import pygamengn

from photo_spawner import PhotoSpawner


@pygamengn.ClassRegistrar.register("Slideshow")
class Slideshow(pygamengn.Game):

    def __init__(
            self,
            photo_spawner,
            year_panel,
            bar_panel,
            photo_info_panel,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.running = True
        self.year_panel = year_panel
        self.bar_panel = bar_panel
        self.photo_info_panel = photo_info_panel
        self.photo_spawner = photo_spawner
        self.photo_spawner.set_year_panel(year_panel, bar_panel)
        self.photo_spawner.set_info_panel(photo_info_panel)
        self.photo_spawner.move_to_next_photo()
        self.is_paused = False

    def update(self, delta):
        """Updates the game."""
        self.handle_input()
        if self.photo_spawner.show_info_panel:
            self.photo_info_panel.update(self.screen.get_rect(), delta)
            self.blit_ui(self.photo_info_panel)

        self.bar_panel.update(self.screen.get_rect(), delta if not self.is_paused else 0)
        self.blit_ui(self.bar_panel)
        self.year_panel.update(self.screen.get_rect(), delta if not self.is_paused else 0)
        self.blit_ui(self.year_panel)

        if not self.is_paused:
            self.year_panel.update(self.screen.get_rect(), delta)
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
                    self.photo_spawner.show_info_panel = not self.photo_spawner.show_info_panel
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_paused = not self.is_paused
