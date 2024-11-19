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
        self.handle_input()
        return super().update(delta)

    def handle_input(self):
        """Reads and handles input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.exit_callback()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.process_mouse_event(event.pos, event.type):
                    self.start_callback()
                elif self.exit_button.process_mouse_event(event.pos, event.type):
                    self.exit_callback()
            elif event.type == pygame.MOUSEMOTION:
                self._component.process_mouse_event(event.pos, event.type)
            elif event.type == pygame.VIDEORESIZE:
                self._component.resize_to_parent(pygame.Rect(0, 0, event.w, event.h))

    def set_start_callback(self, start_callback):
        """Sets the function to call when the start button is clicked."""
        self.start_callback = start_callback

    def set_exit_callback(self, exit_callback):
        """Sets the function to call when the exit button is clicked."""
        self.exit_callback = exit_callback
