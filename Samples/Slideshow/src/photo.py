from enum import StrEnum, auto

import numpy

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject
from pygamengn.interpolator import Interpolator, InterpolationMode
from pygamengn.mover import MoverTime



class State(StrEnum):
    FLYING_IN = auto()
    ON_DISPLAY = auto()
    FLYING_OUT = auto()
    INACTIVE = auto()


class MoveSpec():
    def __init__(
        self,
        normalized_dest,
        revolutions,
        duration,
        move_interpolation_mode,
        centre_offset = pygame.Vector2(0, 0)
    ):
        self.normalized_dest = normalized_dest
        self.revolutions = revolutions
        self.duration = duration
        self.move_interpolation_mode = move_interpolation_mode

        screen_rect = pygame.display.get_surface().get_rect()
        self.dest = pygame.Vector2(
            screen_rect.width * self.normalized_dest[0],
            screen_rect.height * self.normalized_dest[1]
        ) - centre_offset


@ClassRegistrar.register("Photo")
class Photo(GameObject):

    def __init__(
        self,
        mover,
        date,
        focal_point,
        max_scale_override = 2.0,
        move_specs = None,
        state = State.INACTIVE,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.alpha = 0
        self.mover = mover
        self.date = date
        self.focal_point = pygame.Vector2(focal_point)
        self.max_scale_override = max_scale_override
        self.move_specs = move_specs
        self.state = state
        self.max_scale = 1.0
        self.min_scale = 0.1
        self.moving_time = 0
        self.done_callback = None
        self.move_on_display = True
        self.on_display_duration = 0

        # Get maximum scale so that the photo fits the screen
        screen_size = pygame.display.get_surface().get_rect().size
        scale_width = screen_size[0] / self.rect.width
        scale_height = screen_size[1] / self.rect.height
        if scale_width < scale_height:
            self.max_scale = scale_width
            self.min_scale = scale_width / 2.0
        else:
            self.max_scale = scale_height
            self.min_scale = scale_height / 2.0
        self.set_scale(self.min_scale)


    def update(self, delta):
        super().update(delta)

        if self.state != State.INACTIVE and self.visible:
            if self.state == State.FLYING_IN:
                self.fly_in(delta)

            elif self.state == State.ON_DISPLAY:
                self.display(delta)

            elif self.state == State.FLYING_OUT:
                self.fly_out(delta)

            self.moving_time += delta


    def start_moving(self, durations, done_callback):
        # This function is a hot mess; it should be cleaned up. But hey, it works in its own brittle way...
        screen_rect = pygame.display.get_surface().get_rect()
        if self.max_scale < 1.3:
            self.display_max_scale = min(self.max_scale * 2.0, self.max_scale_override)
            r = self.image_asset.get_rect().copy()
            r = r.scale_by(self.display_max_scale)
            offset = pygame.Vector2(
                (self.focal_point.x - 0.5) * r.width,
                (self.focal_point.y - 0.45) * r.height
            )
        else:
            self.display_max_scale = self.max_scale
            offset = pygame.Vector2(0, 0)

        self.move_on_display = numpy.random.choice([True, False])

        move_specs = {
            "flying_in": MoveSpec(
                normalized_dest = pygame.Vector2(0.5, 0.5),
                revolutions = 0,
                duration = durations["flying_in"],
                move_interpolation_mode = InterpolationMode.EASE_OUT,
                centre_offset = pygame.Vector2(0, 0) if self.move_on_display else offset
            ),
            "on_display": MoveSpec(
                normalized_dest = pygame.Vector2(0.5, 0.5),
                revolutions = 0,
                duration = durations["on_display"],
                move_interpolation_mode = InterpolationMode.EASE_OUT,
                centre_offset = offset if self.move_on_display else pygame.Vector2(0, 0)

            ),
            "flying_out": MoveSpec(
                normalized_dest = (1.1, numpy.random.random_sample()),
                revolutions = 0, # numpy.random.random() * 2 * numpy.random.choice([1, -1]),
                duration = durations["flying_out"],
                move_interpolation_mode = InterpolationMode.EASE_OUT,
            ),
        }
        self.move_specs = move_specs
        self.visible = True
        self.done_callback = done_callback
        self.position = pygame.Vector2(0, numpy.random.random_integers(0, screen_rect.height))
        self.transform()
        self.on_display_duration = self.move_specs[State.ON_DISPLAY].duration
        self.state_transition(State.FLYING_IN)


    def state_transition(self, to_state):
        # This function is a hot mess; it should be cleaned up. But hey, it works in its own brittle way...
        screen_rect = pygame.display.get_surface().get_rect()
        self.mover = MoverTime(
            self.move_specs[to_state].duration,
            self.position,
            self.move_specs[to_state].dest,
            self.move_specs[to_state].move_interpolation_mode
        )
        self.state = to_state
        if to_state == State.FLYING_IN or to_state == State.FLYING_OUT:
            self.moving_time = 0
        self.ease_in_interp = Interpolator(self.move_specs[to_state].duration, mode = InterpolationMode.EASE_IN)
        self.ease_out_interp = Interpolator(self.move_specs[to_state].duration, mode = InterpolationMode.EASE_OUT)

        if to_state == State.FLYING_OUT:
            self.scale_interp = Interpolator(
                duration = self.move_specs[to_state].duration,
                from_value = self.scale,
                to_value = 0.001,
                mode = InterpolationMode.EASE_OUT
            )
        elif to_state == State.FLYING_IN:
            self.scale_interp = Interpolator(
                duration = self.move_specs[State.FLYING_IN].duration + self.move_specs[State.ON_DISPLAY].duration,
                from_value = self.min_scale if self.move_on_display else self.display_max_scale,
                to_value = self.display_max_scale if self.move_on_display else self.max_scale,
                mode = InterpolationMode.EASE_OUT
            )
            if not self.move_on_display:
                self.mover.duration = 1
        elif to_state == State.ON_DISPLAY:
            self.ease_out_interp = Interpolator(
                duration = self.move_specs[State.FLYING_IN].duration,
                mode = InterpolationMode.EASE_IN
            )


    def fly_in(self, delta):
        self.position = self.mover.move(delta)
        if self.mover.is_arrived():
            self.state_transition(State.ON_DISPLAY)
        else:
            factor = self.ease_in_interp.get(self.moving_time)
            self.set_alpha(factor)
            self.set_scale(self.scale_interp.get(self.moving_time))


    def display(self, delta):
        self.position = self.mover.move(delta)
        if self.move_on_display:
            if self.mover.is_arrived():
                self.state_transition(State.FLYING_OUT)
                self.done_callback()
        else:
            self.on_display_duration -= delta
            self.set_alpha(self.ease_out_interp.get(self.moving_time))
            if self.on_display_duration <= 0:
                self.state_transition(State.FLYING_OUT)
                self.done_callback()

        self.set_scale(self.scale_interp.get(self.moving_time))


    def fly_out(self, delta):
        self.position = self.mover.move(delta)

        factor = self.ease_out_interp.get(self.moving_time)
        self.set_alpha(1.0 - factor)
        self.set_scale(self.scale_interp.get(self.moving_time))
        self.heading = 360.0 * self.move_specs[State.FLYING_OUT].revolutions * factor

        if self.mover.is_arrived():
            # I should've exited the screen -> make sure I'm off the screen so I get deleted
            screen_rect = pygame.display.get_surface().get_rect()
            self.position.x = screen_rect.width * 4
            self.transform()
            self.state = State.INACTIVE
