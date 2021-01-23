import pygame

from UI.panel import ColourPanel
from UI.spinner import Spinner
from class_registrar import ClassRegistrar


@ClassRegistrar.register("DebriefPanel")
class DebriefPanel(ColourPanel):
    """Debrief panel to show after a rounds ends."""

    def __init__(self, asteroid_spawner, **kwargs):
        super().__init__(**kwargs)
        self.bind_children()
        self.asteroid_spawner = asteroid_spawner
        self.continue_callback = None
        self.score = 0
        self.time = 0
        self.asteroid_count = 0
        self.waypoint_count = 0

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
                self.continue_callback()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.continue_button.rect.collidepoint(mouse_pos):
                    self.continue_callback()

    def set_continue_callback(self, continue_callback):
        """Sets the function to call when the continue button is clicked."""
        self.continue_callback = continue_callback

    def set_score_data(self, score, time, asteroid_count, waypoint_count):
        """Sets the data that is to be compiled into a final score."""
        self.score = score
        self.time = time
        self.asteroid_count = asteroid_count
        self.waypoint_count = waypoint_count
