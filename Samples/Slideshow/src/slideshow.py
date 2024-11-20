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

        self.slideshow_ui = slideshow_ui
        self.photo_info_ui = photo_info_ui
        self.show_ui(self.slideshow_ui, 500)

        self.photo_spawner = photo_spawner
        self.photo_spawner.set_slideshow_ui(slideshow_ui)
        self.photo_spawner.set_info_ui(photo_info_ui)
        self.photo_spawner.move_to_next_photo()

    def update(self, delta):
        """Updates the game."""
        if not self._is_paused:
            self.photo_spawner.update(delta)
            if self.photo_spawner.done:
                self.exit_game()
        super().update(delta)

    def handle_event(self, event: pygame.event) -> bool:
        rv = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit_game()
                rv = True
            elif event.key == pygame.K_RIGHT:
                self.photo_spawner.move_to_next_photo()
                rv = True
            elif event.key == pygame.K_LEFT:
                self.photo_spawner.move_to_prev_photo()
                rv = True
            elif event.key == pygame.K_i:
                self.photo_spawner.show_info_ui = self.toggle_ui(self.photo_info_ui, 200)
                rv = True
            elif event.key == pygame.K_SPACE:
                self.toggle_pause()
                rv = True
        if not rv:
            rv = super().handle_event(event)
        return rv
