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

    def handle_event(self, event: pygame.event) -> bool:
        rv = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.resume_callback()
            rv = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.resume_button.process_mouse_event(event.pos, event.type):
                self.resume_callback()
                rv = True
            elif self.exit_button.process_mouse_event(event.pos, event.type):
                self.exit_callback()
                rv = True
        else:
            rv = super().handle_event(event)
        return rv

    def set_resume_callback(self, resume_callback):
        """Sets the function to call when the resume button is clicked."""
        self.resume_callback = resume_callback

    def set_exit_callback(self, exit_callback):
        """Sets the function to call when the exit button is clicked."""
        self.exit_callback = exit_callback
