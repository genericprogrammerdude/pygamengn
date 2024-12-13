import pygame

from pygamengn.UI.root import Root
from pygamengn.class_registrar import ClassRegistrar


@ClassRegistrar.register("MainMenu")
class MainMenu(Root):
    """Main menu UI."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.exit_callback = None
        self.count = 0

    def update(self, delta) -> bool:
        """Updates the main menu."""
        keep_updating = super().update(delta)
        if not keep_updating:
            print(f"MainMenu is done but let's keep going")
            self.fade_in(500)
        return True

    def set_parent_rect(self, rect: pygame.Rect):
        super().set_parent_rect(rect)
        self._set_uniform_font_size([self.start_text, self.exit_text], 0.8)

    def handle_event(self, event: pygame.event) -> bool:
        """Reads and handles input."""
        rv = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit_callback()
                rv = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.process_mouse_event(event.pos, event.type):
                self.exit_text.text = "Click me to exit!"
                self.spinner_panel.set_visible(not self.spinner_panel.visible)
                self.exit_button.set_border(0.01, (250, 100, 150))
                self.count += 1
                if self.count % 2 != 0:
                    self.fade_out(500)
                else:
                    self.fade_in(500)
                rv = True
            elif self.exit_button.process_mouse_event(event.pos, event.type):
                self.exit_callback()
                rv = True
        else:
            rv = super().handle_event(event)
        return rv

    def set_exit_callback(self, exit_callback):
        """Sets the function to call when the exit button is clicked."""
        self.exit_callback = exit_callback
