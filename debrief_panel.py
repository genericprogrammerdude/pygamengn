import pygame

from UI.panel import ColourPanel
from class_registrar import ClassRegistrar


@ClassRegistrar.register("DebriefPanel")
class DebriefPanel(ColourPanel):
    """Debrief panel to show after a rounds ends."""

    def __init__(self, asteroid_spawner, **kwargs):
        super().__init__(**kwargs)
        self.asteroid_spawner = asteroid_spawner
        self.continue_button = self.children[0]
        self.continue_callback = None

    def update(self, parent_rect, delta):
        """Updates the main menu."""
        super().update(parent_rect, delta)
        self.handle_input()
        self.asteroid_spawner.update(delta)

    def handle_input(self):
        """Reads and handles input."""
        mouse_pos = pygame.mouse.get_pos()
        self.propagate_mouse_pos(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.cotinue_callback()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.continue_button.rect.collidepoint(mouse_pos):
                    self.continue_callback()

    def set_continue_callback(self, continue_callback):
        """Sets the function to call when the continue button is clicked."""
        self.continue_callback = continue_callback
