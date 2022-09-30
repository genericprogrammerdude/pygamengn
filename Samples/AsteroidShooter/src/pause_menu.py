import pygame

from pygamengn.UI.panel import ColourPanel
from pygamengn.class_registrar import ClassRegistrar


@ClassRegistrar.register("PauseMenu")
class PauseMenu(ColourPanel):
    """Pause menu UI."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind_children()
        self.resume_callback = None
        self.exit_callback = None

    def update(self, parent_rect, delta):
        """Updates the main menu."""
        super().update(parent_rect, delta)
        self.handle_input()

    def handle_input(self):
        """Reads and handles input."""
        mouse_pos = pygame.mouse.get_pos()
        self.propagate_mouse_pos(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_callback()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.resume_callback()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.resume_button.rect.collidepoint(mouse_pos):
                    self.resume_callback()
                elif self.exit_button.rect.collidepoint(mouse_pos):
                    self.exit_callback()

    def set_resume_callback(self, resume_callback):
        """Sets the function to call when the resume button is clicked."""
        self.resume_callback = resume_callback

    def set_exit_callback(self, exit_callback):
        """Sets the function to call when the exit button is clicked."""
        self.exit_callback = exit_callback
