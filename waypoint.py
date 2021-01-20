import random

from game_object_factory import GameObjectFactory
from trigger import Trigger


@GameObjectFactory.register("Waypoint")
class Waypoint(Trigger):
    """A trigger triggers actions when game objects enter them."""

    def __init__(self, distance, angular_velocity, **kwargs):
        super().__init__(**kwargs)
        self.distance = distance
        self.angular_velocity = angular_velocity * random.choice([-1, 1]) * (random.random() + 0.5)

    def update(self, delta):
        super().update(delta)
        heading = (self.heading + delta * self.angular_velocity / 1000.0) % 360
        self.set_heading(heading)
