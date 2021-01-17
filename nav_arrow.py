from game_object import GameObject
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("NavArrow")
class NavArrow(GameObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_target(self, target):
        """Sets the target to point to."""
        self.target = target
