import pygame

from pygamengn.UI.root import Root
from pygamengn.class_registrar import ClassRegistrar


@ClassRegistrar.register("PauseMenu")
class PauseMenu(Root):
    """Pause menu UI."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.resume_callback = None
        self.main_menu_callback = None

    def set_parent_rect(self, rect: pygame.Rect):
        super().set_parent_rect(rect)
        self._set_uniform_font_size([self.resume_text, self.main_menu_text], 0.6)

    def handle_event(self, event: pygame.event.Event) -> bool:
        rv = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.resume_callback(event.touch)
            rv = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.resume_button.process_mouse_event(event.pos, event.type):
                self.resume_callback(event.touch)
                rv = True
            elif self.main_menu_button.process_mouse_event(event.pos, event.type):
                self.main_menu_callback()
                rv = True
        else:
            rv = super().handle_event(event)
        return rv

    def set_resume_callback(self, resume_callback):
        """Sets the function to call when the resume button is clicked."""
        self.resume_callback = resume_callback

    def set_main_menu_callback(self, main_menu_callback):
        """Sets the function to call when the main_menu button is clicked."""
        self.main_menu_callback = main_menu_callback

