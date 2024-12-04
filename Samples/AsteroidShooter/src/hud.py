import logging

import pygame

from pygamengn.class_registrar import ClassRegistrar

from pygamengn.UI.root import Root


@ClassRegistrar.register("Hud")
class Hud(Root):
    """HUD UI."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.heading = 0
        self._joystick_finger = -1
        self._fire = False
        self.__zero_angle = pygame.Vector2(1, 0)
        self._joystick_motion = False


    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handles the given input event."""
        rv = False

        if self.joystick.active:
            if event.type == pygame.FINGERDOWN:
                if event.x < 0.6:
                    self._update_heading(event.x, event.y, True)
                    self._joystick_finger = event.finger_id
                else:
                    self._fire = True
                rv = True

            elif event.type == pygame.FINGERUP:
                if event.finger_id == self._joystick_finger:
                    self._joystick_finger = -1
                    self._joystick_motion = False
                    rv = True

            elif event.type == pygame.FINGERMOTION:
                if event.finger_id == self._joystick_finger:
                    self._update_heading(event.x, event.y)
                    self._joystick_motion = True
                rv = True

        return rv


    def _update_heading(self, x: int, y: int, in_stick_panel: bool = False):
        finger_pos = pygame.Vector2(
            x * self._component.rect.width,
            y * self._component.rect.height
        )
        diff = finger_pos - pygame.Vector2(self.stick.rect.center)
        if not in_stick_panel or diff.magnitude() < self.stick.rect.width / 2:
            theta = self.__zero_angle.angle_to(diff)
            self.heading = -theta - 90
            self.ship.angle = self.heading


    @property
    def joystick_motion(self) -> bool:
        return self._joystick_motion


    @property
    def touch_joystick_active(self) -> bool:
        return self.joystick.active


    @property
    def fire(self) -> bool:
        """
        Returns True if there was fire input.

        Because the fire action is single shot, the underlying variable is set to false after a True value is returned.
        """
        rv = self._fire
        self._fire = False
        return rv


    def fade_in(self, duration: int):
        super().fade_in(duration)
        self.heading = 0
        self.ship.angle = 0
        self._joystick_motion = False
        self._joystick_finger = -1
        self._fire = False


    def set_joystick_state(self, state: bool):
        self.joystick.active = state
