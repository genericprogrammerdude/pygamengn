from enum import StrEnum, auto

import numpy

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject



class State(StrEnum):
    FLYING_IN = auto()
    ON_DISPLAY = auto()
    FLYING_OUT = auto()
    INACTIVE = auto()


class MoveSpec():
    def __init__(self, normalized_dest, revolutions, duration):
        self.normalized_dest = normalized_dest
        self.revolutions = revolutions
        self.duration = duration

        screen_rect = pygame.display.get_surface().get_rect()
        self.dest = pygame.Vector2(
            screen_rect.width * self.normalized_dest[0],
            screen_rect.height * self.normalized_dest[1]
        )


@ClassRegistrar.register("Photo")
class Photo(GameObject):

    def __init__(self, mover, date, focal_point, move_specs = None, state = State.INACTIVE, **kwargs):
        super().__init__(**kwargs)
        self.alpha = 0
        self.mover = mover
        self.date = date
        self.focal_point = focal_point
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
        self.mover.initialize(self.move_specs[to_state].duration, self.position, self.move_specs[to_state].dest)
        self.state = to_state
        self.moving_time = 0


    def fly_in(self, delta):
        self.position = self.mover.move(delta)
        if self.mover.is_arrived():
            # Set up the mover for displaying the photo
            self.state_transition(State.ON_DISPLAY)
            self.set_alpha(1.0)
            self.set_scale(self.max_scale)
            self.heading = 0

        else:
            # Animate alpha, scale, and heading
            theta = self.moving_time * numpy.pi / self.move_specs[State.FLYING_IN].duration
            factor = (1.0 - numpy.cos(theta)) / 2.0
            self.set_alpha(factor)
            self.set_scale(self.min_scale + factor * (self.max_scale - self.min_scale))

            theta = self.moving_time * (numpy.pi / 2.0) / self.move_specs[State.FLYING_IN].duration
            factor = numpy.sin(theta)
            self.heading = 360.0 * self.move_specs[State.FLYING_IN].revolutions * factor


    def display(self, delta):
        self.position = self.mover.move(delta)
        if self.mover.is_arrived():
            self.state_transition(State.FLYING_OUT)


    def fly_out(self, delta):
        self.position = self.mover.move(delta)

        theta = self.moving_time * numpy.pi / self.move_specs[State.FLYING_OUT].duration
        factor = (1.0 - numpy.cos(theta)) / 2.0
        self.set_alpha(1.0 - factor)
        self.set_scale(self.max_scale - factor * (self.max_scale - self.min_scale))

        theta = self.moving_time * (numpy.pi / 2.0) / self.move_specs[State.FLYING_OUT].duration
        factor = numpy.sin(theta)
        self.heading = 360.0 * self.move_specs[State.FLYING_OUT].revolutions * factor

        if self.mover.is_arrived():
            # I should've exited the screen -> make sure I'm off the screen so I get deleted
            screen_rect = pygame.display.get_surface().get_rect()
            self.position.x = screen_rect.width * 4
            self.transform()
            self.state = State.INACTIVE


    def start_moving(self, move_spec):
        move_specs = {
            "flying_in": MoveSpec(
                normalized_dest = (0.25, 0.5),
                revolutions = numpy.random.randint(4, 10) * numpy.random.choice([1, -1]),
                duration = 2000,
            ),
            "on_display": MoveSpec(
                normalized_dest = (0.75, 0.5),
                revolutions = 0,
                duration = 4000,
            ),
            "flying_out": MoveSpec(
                normalized_dest = (1.0, 0.5),
                revolutions = numpy.random.randint(4, 10) * numpy.random.choice([1, -1]),
                duration = 2000,
            ),
        }
        self.move_specs = move_specs
        self.visible = True
        self.state_transition(State.FLYING_IN)
