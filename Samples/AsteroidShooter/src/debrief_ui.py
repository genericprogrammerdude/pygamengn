import pygame

from pygamengn.UI.root import Root
from pygamengn.class_registrar import ClassRegistrar


@ClassRegistrar.register("DebriefUI")
class DebriefUI(Root):
    """Debrief UI to show after a rounds ends."""

    def __init__(self, asteroid_spawner, **kwargs):
        super().__init__(**kwargs)
        self.asteroid_spawner = asteroid_spawner
        self.continue_callback = None
        self.score = 0
        self.time = 0
        self.asteroid_count = 0
        self.waypoint_count = 0
        self.asteroid_multiplier = 0
        self.waypoint_multiplier = 0

    def update(self, delta: int) -> bool:
        """Updates the main menu."""
        self.handle_input()
        self.asteroid_spawner.update(delta)
        return super().update(delta)

    def handle_input(self):
        """Reads and handles input."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.continue_callback()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button.process_mouse_event(event.pos, event.type):
                    self.continue_callback()
            elif event.type == pygame.MOUSEMOTION:
                self._component.process_mouse_event(event.pos, event.type)
            elif event.type == pygame.VIDEORESIZE:
                self._component.resize_to_parent(pygame.Rect(0, 0, event.w, event.h))

    def set_continue_callback(self, continue_callback):
        """Sets the function to call when the continue button is clicked."""
        self.continue_callback = continue_callback

    def set_score_data(self, score, time, asteroid_count, waypoint_count, asteroid_multiplier, waypoint_multiplier):
        """Sets the data that is to be compiled into a final score."""
        self.score = score
        self.time = time
        self.asteroid_count = asteroid_count
        self.waypoint_count = waypoint_count
        self.asteroid_multiplier = asteroid_multiplier
        self.waypoint_multiplier = waypoint_multiplier

        self.asteroid_count_text.text = f"{asteroid_count}"
        self.waypoint_count_text.text = f"{waypoint_count}"
        self.asteroid_multiplier_text.text = f"x{asteroid_multiplier}"
        self.waypoint_multiplier_text.text = f"x{waypoint_multiplier}"
        self.asteroid_total_text.text = f"{asteroid_count * asteroid_multiplier}"
        self.waypoint_total_text.text = f"{waypoint_count * waypoint_multiplier}"

        self.total_score_text.text = f"{score + asteroid_count * asteroid_multiplier + waypoint_count * waypoint_multiplier}"
