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
        self.joystick_active = False
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
        if event.type == pygame.MOUSEMOTION:
            # <Event(1024-MouseMotion {'pos': (998, 456), 'rel': (1, -2), 'buttons': (0, 0, 0), 'touch': False, 'window': None})>
            # mouse_pos = event.pos
            # input_rect = self.joystick.rect
            # diff = mouse_pos - pygame.Vector2(input_rect.center)
            # if diff.magnitude() < input_rect.width / 2:
            #     r, theta = diff.as_polar()
            #     self.heading = -theta - 90
            #     if not self.joystick_active:
            #         self._vel_interp = AutoInterpolator(self._velocity_decay_ms, 1, 0)
            #         self.joystick_active = True
            #     rv = True
            # else:
            #     self.joystick_active = False
            pass

        elif event.type == pygame.FINGERDOWN:
            if event.x < 0.5:
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
                # <Event(1794-FingerMotion {'touch_id': 65679, 'finger_id': 354, 'x': 0.22499999403953552, 'y': 0.7736111283302307, 'dx': 0.0, 'dy': -0.001388847827911377, 'pressure': -0.001388847827911377, 'window': None})>
                dv = pygame.Vector2(event.dx, event.dy)
                r, theta = dv.as_polar()
                if r > 0.002:
                    self.heading = -theta - 90
                    if not self.joystick_active:
                        self._vel_interp = AutoInterpolator(self._velocity_decay_ms, 1, 0)
                    rv = True
                logging.info(f"r, theta == {r}, {theta}")

        self.joystick_active = self._joystick_finger != -1
        return rv


    @property
    def fire(self) -> bool:
        """
        Returns True if there was fire input.

        Because the fire action is single shot, the underlying variable is set to false after a True value is returned.
        """
        rv = self._fire
        self._fire = False
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
        self.joystick_active = False
        self._fire = False
