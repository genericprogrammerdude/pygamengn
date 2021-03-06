import random

from class_registrar import ClassRegistrar
from trigger import Trigger


@ClassRegistrar.register("Waypoint")
class Waypoint(Trigger):
    """A trigger triggers actions when game objects enter them."""

    def __init__(self, distance, angular_velocity, digit_image_assets, **kwargs):
        super().__init__(**kwargs)
        self.distance = distance
        self.angular_velocity = angular_velocity * random.choice([-1, 1]) * (random.random() + 0.5)
        self.digit_image_assets = digit_image_assets
        self.number = 1
        self.dirty_number = False

    def update(self, delta):
        heading = (self.heading + delta * self.angular_velocity / 1000.0) % 360
        self.heading = heading
        super().update(delta)

        if self.dirty_number:
            self.dirty_number = False
            if self.number > 99:
                self.number = 0
            tens = self.number // 10
            ones = self.number % 10
            self.attachments[0].game_object.set_image(self.digit_image_assets[tens])
            self.attachments[1].game_object.set_image(self.digit_image_assets[ones])

    def set_number(self, number):
        """Sets the number to display on the waypoint."""
        self.number = number
        self.dirty_number = True
