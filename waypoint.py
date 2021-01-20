import random

from game_object_factory import GameObjectFactory
from trigger import Trigger


@GameObjectFactory.register("Waypoint")
class Waypoint(Trigger):
    """A trigger triggers actions when game objects enter them."""

    def __init__(self, distance, angular_velocity, digit_image_assets, **kwargs):
        super().__init__(**kwargs)
        self.distance = distance
        self.angular_velocity = angular_velocity * random.choice([-1, 1]) * (random.random() + 0.5)
        self.digit_image_assets = digit_image_assets

    def update(self, delta):
        heading = (self.heading + delta * self.angular_velocity / 1000.0) % 360
        self.set_heading(heading)
        super().update(delta)

    def set_number(self, number):
        """Sets the number to display on the waypoint."""
        if number > 99:
            number = 0
        tens = number // 10
        ones = number % 10
        self.attachments[0].game_object.set_image(self.digit_image_assets[tens])
        self.attachments[1].game_object.set_image(self.digit_image_assets[ones])
