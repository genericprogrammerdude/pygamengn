import logging

import pygame

from pygame._sdl2 import touch

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
        self._joystick_finger = -1
        self._fire = False


    def update(self, delta: int) -> bool:
        if self.joystick_active:
            self.velocity_multiplier = 1
        else:
            self.velocity_multiplier = self._vel_interp.update(delta)
        return super().update(delta)


    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handles the given input event."""
        rv = False
        if event.type == pygame.FINGERDOWN:
            if self._process_finger(event.x, event.y):
                self._joystick_finger = event.finger_id
            else:
                self._fire = True
            rv = True

        elif event.type == pygame.FINGERUP:
            if event.finger_id == self._joystick_finger:
                self._joystick_finger = -1
                rv = True

        elif event.type == pygame.FINGERMOTION:
            if event.finger_id == self._joystick_finger:
                processed = self._process_finger(event.x, event.y)
                if not processed:
                    self._joystick_finger = -1
            rv = True

        return rv


    def _process_finger(self, x: int, y: int) -> bool:
        rv = False
        finger_pos = pygame.Vector2(
            x * self._component.rect.width,
            y * self._component.rect.height
        )
        input_rect = self.joystick.rect
        diff = finger_pos - pygame.Vector2(input_rect.center)
        r, theta = diff.as_polar()
        if r < input_rect.width / 2:
            self.heading = -theta - 90
            self.ship.angle = self.heading
            rv = True
        return rv


    @property
    def joystick_active(self) -> bool:
        return self._joystick_finger != -1


    @property
    def fire(self) -> bool:
        """
        Returns True if there was fire input.

        Because the fire action is single shot, the underlying variable is set to false after a True value is returned.
        """
        rv = self._fire
        self._fire = False
        return rv


    @property
    def joystick_motion(self) -> pygame.Vector2:
        rv = self._joystick_motion.copy()
        self._joystick_motion.update(0, 0)
        return rv


    def activate(self) -> bool:
        """This is invoked when the input handler becomes active."""
        super().activate()
        self._initialize_state()


    def deactivate(self) -> bool:
        """This is invoked when the input handler is deactivated."""
        super().deactivate()
        self._initialize_state()


    def _initialize_state(self):
        self._joystick_finger = -1
        self._fire = False
