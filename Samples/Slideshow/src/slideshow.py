import pygame
import pygamengn

from photo_spawner import PhotoSpawner


@pygamengn.ClassRegistrar.register("Slideshow")
class Slideshow(pygamengn.Game):

    def __init__(
            self,
            photo_spawner,
            year_ui,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.running = True
        self.year_ui = year_ui
        self.photo_spawner = photo_spawner
        self.photo_spawner.set_year_text_panel(year_ui.year_text)

    def update(self, delta):
        """Updates the game."""
        self.handle_input()
        self.photo_spawner.update(delta)
        self.year_ui.update(self.screen.get_rect(), delta)
        self.blit_ui(self.year_ui)
        super().update(delta)

        if self.photo_spawner.done and len(self.render_group.sprites()) == 0:
            self.running = False

    def handle_input(self):
        """Reads input and makes things happen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
