from game_object import GameObject
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("NavArrow")
class NavArrow(GameObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_target(self, target):
        """Sets the target to point to."""
        self.target = target

    def update(self, delta):
        super().update(delta)

        if self.target:
            dist_to_target = (self.target.pos - self.pos).length()
            if dist_to_target > 1000:
                self.alpha = 1.0
            else:
                self.alpha = dist_to_target / 1000.0
