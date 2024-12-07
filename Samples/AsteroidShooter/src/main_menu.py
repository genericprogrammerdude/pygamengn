import sys

import pygame

from pygamengn.class_registrar import ClassRegistrar

from pygamengn.UI.panel import Panel
from pygamengn.UI.root import Root

from asteroid import AsteroidSpawner


@ClassRegistrar.register("MainMenu")
class MainMenu(Root):
    """Main menu UI."""

    def __init__(self, asteroid_spawner, **kwargs):
        super().__init__(**kwargs)
        self.asteroid_spawner = asteroid_spawner
        self.start_callback = None
        self.exit_callback = None
        if sys.platform == "emscripten":
            # No need for an Exit button when running as a web app
            self._component.delete_child(self.exit_button)
            self.exit_button = None
            self.start_button._normalized_pos = pygame.Vector2()
            self.start_button.vert_align = Panel.VertAlign.CENTRE
            self.start_button.horz_align = Panel.HorzAlign.CENTRE

    def update(self, delta: int) -> bool:
        """Updates the main menu."""
        self.asteroid_spawner.update(delta)
        return super().update(delta)

    def set_parent_rect(self, rect: pygame.Rect):
        super().set_parent_rect(rect)
        self._set_uniform_font_size(
            [self.start_text, self.exit_text] if self.exit_button else [self.start_text],
            0.6
        )

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handles the given input event."""
        rv = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.exit_button:
                self.exit_callback()
            rv = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.process_mouse_event(event.pos, event.type):
                self.start_callback(event.touch)
                rv = True
            elif self.exit_button and self.exit_button.process_mouse_event(event.pos, event.type):
                self.exit_callback()
                rv = True
        if not rv:
            rv = super().handle_event(event)
        return rv

    def set_start_callback(self, start_callback):
        """Sets the function to call when the start button is clicked."""
        self.start_callback = start_callback

    def set_exit_callback(self, exit_callback):
        """Sets the function to call when the exit button is clicked."""
        self.exit_callback = exit_callback
