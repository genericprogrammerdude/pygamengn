from game_object import GameObject
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("NavArrow")
class NavArrow(GameObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.waypoint = None

    def set_waypoint(self, waypoint):
        """Sets the waypoint to point to."""
        self.waypoint = waypoint

    def update(self, delta):
        super().update(delta)

        if self.waypoint and self.parent:
            diff = self.waypoint.pos - self.parent.pos
            dist_to_target = diff.length()
            direction = diff / dist_to_target

            self.set_pos(self.parent.pos + direction * 150)

            _, angle = direction.as_polar()
            self.set_heading(270 - angle)

            dist_to_target = diff.length()
            if dist_to_target > 1000:
                self.alpha = 1.0
            else:
                self.alpha = dist_to_target / 1000.0

        else:
            self.alpha = 0
