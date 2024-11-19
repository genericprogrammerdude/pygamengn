import pygame

from pygamengn.UI.root import Root
from pygamengn.class_registrar import ClassRegistrar


@ClassRegistrar.register("PauseMenu")
class PauseMenu(Root):
    """Pause menu UI."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resume_callback = None
        self.exit_callback = None

    def update(self, delta: int) -> bool:
        """Updates the main menu."""
        self.handle_input()
        return super().update(delta)

    def handle_input(self):
        """Reads and handles input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_callback()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.resume_callback()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.resume_button.process_mouse_event(event.pos, event.type):
                    self.resume_callback()
                elif self.exit_button.process_mouse_event(event.pos, event.type):
                    self.exit_callback()
            elif event.type == pygame.MOUSEMOTION:
                self._component.process_mouse_event(event.pos, event.type)
            elif event.type == pygame.VIDEORESIZE:
                self._component.resize_to_parent(pygame.Rect(0, 0, event.w, event.h))

    def set_resume_callback(self, resume_callback):
        """Sets the function to call when the resume button is clicked."""
        self.resume_callback = resume_callback

    def set_exit_callback(self, exit_callback):
        """Sets the function to call when the exit button is clicked."""
        self.exit_callback = exit_callback
