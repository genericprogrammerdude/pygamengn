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

    def __init__(self, mover, date, focal_point, move_specs = None, state = State.INACTIVE, **kwargs):
        super().__init__(**kwargs)
        self.alpha = 0
        self.mover = mover
        self.date = date
        self.focal_point = pygame.Vector2(focal_point)
        self.move_specs = move_specs
        self.state = state
        self.max_scale = 1.0
        self.min_scale = 0.1
        self.moving_time = 0

        # Get maximum scale so that the photo fits the screen
        screen_size = pygame.display.get_surface().get_rect().size
        scale_width = screen_size[0] / self.rect.width
        scale_height = screen_size[1] / self.rect.height
        if scale_width < scale_height:
            self.max_scale = scale_width
            self.min_scale = scale_width / 4.0
        else:
            self.max_scale = scale_height
            self.min_scale = scale_height / 4.0
        self.set_scale(self.min_scale)


    def start_moving(self):
        screen_rect = pygame.display.get_surface().get_rect()
        if self.max_scale < 1.7:
            self.display_max_scale = self.max_scale * 2.0
            r = self.image_asset.get_rect().copy()
            r = r.scale_by(self.display_max_scale)
            offset = pygame.Vector2(
                (self.focal_point.x - 0.5) * r.width,
                (self.focal_point.y - 0.45) * r.height
            )
        else:
            self.display_max_scale = self.max_scale
            offset = pygame.Vector2(0, 0)

        move_specs = {
            "flying_in": MoveSpec(
                normalized_dest = pygame.Vector2(0.5, 0.5),
                revolutions = numpy.random.randint(1, 2) * numpy.random.choice([1, -1]),
                duration = 2000,
                move_interpolation_mode = InterpolationMode.EASE_OUT,
            ),
            "on_display": MoveSpec(
                normalized_dest = pygame.Vector2(0.5, 0.5),
                revolutions = 0,
                duration = 40000,
                move_interpolation_mode = InterpolationMode.EASE_OUT,
                centre_offset = offset

            ),
            "flying_out": MoveSpec(
                normalized_dest = (1.1, numpy.random.random_sample()),
                revolutions = numpy.random.randint(1, 2) * numpy.random.choice([1, -1]),
                duration = 2000,
                move_interpolation_mode = InterpolationMode.EASE_OUT,
            ),
        }
        self.move_specs = move_specs
        self.visible = True
        self.position = pygame.Vector2(0, numpy.random.random_integers(0, screen_rect.height))
        self.transform()
        self.state_transition(State.FLYING_IN)


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


    def state_transition(self, to_state):
        screen_rect = pygame.display.get_surface().get_rect()
        self.mover = MoverTime(
            self.move_specs[to_state].duration,
            self.position,
            self.move_specs[to_state].dest,
            self.move_specs[to_state].move_interpolation_mode
        )
        self.state = to_state
        self.moving_time = 0
        self.ease_in_interp = Interpolator(self.move_specs[to_state].duration, mode = InterpolationMode.EASE_IN)
        self.ease_out_interp = Interpolator(self.move_specs[to_state].duration, mode = InterpolationMode.EASE_OUT)

        if to_state == State.FLYING_OUT:
            self.scale_interp = Interpolator(
                duration = self.move_specs[to_state].duration,
                from_value = self.scale,
                to_value = 0.01,
                mode = InterpolationMode.EASE_OUT
            )
        elif to_state == State.ON_DISPLAY:
            self.scale_interp = Interpolator(
                duration = self.move_specs[to_state].duration,
                from_value = self.scale,
                to_value = self.display_max_scale,
                mode = InterpolationMode.EASE_OUT
            )


    def fly_in(self, delta):
        self.position = self.mover.move(delta)
        if self.mover.is_arrived():
            self.state_transition(State.ON_DISPLAY)
            self.set_alpha(1.0)
            self.heading = 0

        else:
            factor = self.ease_in_interp.get(self.moving_time)
            self.set_alpha(factor)
            self.set_scale(self.min_scale + factor * (self.max_scale - self.min_scale))

            factor = self.ease_out_interp.get(self.moving_time)
            # self.heading = 360.0 * self.move_specs[State.FLYING_IN].revolutions * factor


    def display(self, delta):
        self.position = self.mover.move(delta)
        if self.mover.is_arrived():
            self.state_transition(State.FLYING_OUT)

        factor = self.ease_out_interp.get(self.moving_time)
        self.set_scale(self.scale_interp.get(self.moving_time))


    def fly_out(self, delta):
        self.position = self.mover.move(delta)

        factor = self.ease_out_interp.get(self.moving_time)
        self.set_alpha(1.0 - factor)
        self.set_scale(self.scale_interp.get(self.moving_time))

        # self.heading = 360.0 * self.move_specs[State.FLYING_OUT].revolutions * factor

        if self.mover.is_arrived():
            # I should've exited the screen -> make sure I'm off the screen so I get deleted
            screen_rect = pygame.display.get_surface().get_rect()
            self.position.x = screen_rect.width * 4
            self.transform()
            self.state = State.INACTIVE
