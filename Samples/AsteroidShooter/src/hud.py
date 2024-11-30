import pygame

from pygamengn.class_registrar import ClassRegistrar

from pygamengn.interpolator import AutoInterpolator
from pygamengn.UI.root import Root


@ClassRegistrar.register("Hud")
class Hud(Root):
    """HUD UI."""

    def __init__(self, velocity_decay_ms = 1000, **kwargs):
        super().__init__(**kwargs)
        self.heading = 0
        self.velocity_multiplier = 0

        self._velocity_decay_ms = velocity_decay_ms
        self._vel_interp = AutoInterpolator(duration = velocity_decay_ms, from_value = 0, to_value = 0)
        self.joystick_active = False


    def update(self, delta: int) -> bool:
        if self.joystick_active:
            self.velocity_multiplier = 1
        else:
            self.velocity_multiplier = self._vel_interp.update(delta)
        return super().update(delta)


    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handles the given input event."""
        # <Event(1024-MouseMotion {'pos': (998, 456), 'rel': (1, -2), 'buttons': (0, 0, 0), 'touch': False, 'window': None})>
        rv = False
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            input_rect = self.joystick.rect
            diff = mouse_pos - pygame.Vector2(input_rect.center)
            if diff.magnitude() < input_rect.width / 2:
                r, theta = diff.as_polar()
                self.heading = -theta - 90
                if not self.joystick_active:
                    self._vel_interp = AutoInterpolator(self._velocity_decay_ms, 1, 0)
                    self.joystick_active = True
                rv = True
            else:
                self.joystick_active = False
        return rv
