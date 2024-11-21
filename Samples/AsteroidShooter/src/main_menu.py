import pygame

from pygamengn.UI.root import Root
from pygamengn.class_registrar import ClassRegistrar
from asteroid import AsteroidSpawner


@ClassRegistrar.register("MainMenu")
class MainMenu(Root):
    """Main menu UI."""

    def __init__(self, asteroid_spawner, **kwargs):
        super().__init__(**kwargs)
        self.asteroid_spawner = asteroid_spawner
        self.start_callback = None
        self.exit_callback = None

    def update(self, delta: int) -> bool:
        """Updates the main menu."""
        self.asteroid_spawner.update(delta)
        return super().update(delta)

    def set_parent_rect(self, rect: pygame.Rect):
        super().set_parent_rect(rect)
        self._set_uniform_font_size([self.start_text, self.exit_text], 0.6)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handles the given input event."""
        rv = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.exit_callback()
            rv = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.process_mouse_event(event.pos, event.type):
                self.start_callback()
                rv = True
            elif self.exit_button.process_mouse_event(event.pos, event.type):
                self.exit_callback()
                rv = True
        else:
            rv = super().handle_event(event)
        return rv

    def set_start_callback(self, start_callback):
        """Sets the function to call when the start button is clicked."""
        self.start_callback = start_callback

    def set_exit_callback(self, exit_callback):
        """Sets the function to call when the exit button is clicked."""
        self.exit_callback = exit_callback
