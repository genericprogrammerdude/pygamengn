import pygame

from pygamengn.UI.panel import ColourPanel
from pygamengn.class_registrar import ClassRegistrar


@ClassRegistrar.register("MainMenu")
class MainMenu(ColourPanel):
    """Main menu UI."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_callback = None
        self.exit_callback = None

    def update(self, parent_rect, delta):
        """Updates the main menu."""
        self.handle_input()
        super().update(parent_rect, delta)

    def handle_input(self):
        """Reads and handles input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.exit_callback()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.process_mouse_event(event.pos, event.type):
                    self.exit_button_text.text = "Click me to exit!"
                    print(f"clicked on start_button")
                elif self.exit_button.process_mouse_event(event.pos, event.type):
                    self.exit_callback()
            elif event.type == pygame.MOUSEMOTION:
                self.process_mouse_event(event.pos, event.type)

    def set_start_callback(self, start_callback):
        """Sets the function to call when the start button is clicked."""
        self.start_callback = start_callback

    def set_exit_callback(self, exit_callback):
        """Sets the function to call when the exit button is clicked."""
        self.exit_callback = exit_callback
