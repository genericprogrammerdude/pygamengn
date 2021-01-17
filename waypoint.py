from game_object_factory import GameObjectFactory
from trigger import Trigger


@GameObjectFactory.register("Waypoint")
class Waypoint(Trigger):
    """A trigger triggers actions when game objects enter them."""

    def __init__(self, distance, **kwargs):
        super().__init__(**kwargs)
        self.distance = distance
