import pygame

from pygamengn.UI.root import Root
from pygamengn.class_registrar import ClassRegistrar


@ClassRegistrar.register("MainMenu")
class MainMenu(Root):
    """Main menu UI."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_callback = None
        self.exit_callback = None
        self.count = 0

    def update(self, delta) -> bool:
        """Updates the main menu."""
        self.handle_input()
        keep_updating = super().update(delta)
        if not keep_updating:
            print(f"MainMenu is done but let's keep going")
            self.fade_in(500)
        return True

    def handle_input(self):
        """Reads and handles input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.exit_callback()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.process_mouse_event(event.pos, event.type):
                    self.exit_button_text.text = "Click me to exit!"
                    self.count += 1
                    if self.count % 2 != 0:
                        self.fade_out(500)
                    else:
                        self.fade_in(500)
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
