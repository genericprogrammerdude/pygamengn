from class_registrar import ClassRegistrar
from game_object import GameObject


@ClassRegistrar.register("NavArrow")
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
            self.visible = True
            diff = self.waypoint.position - self.parent.position
            dist_to_target = diff.length()
            direction = diff / dist_to_target

            self.position = self.parent.position + direction * 150

            _, angle = direction.as_polar()
            self.set_heading(270 - angle)

            dist_to_target = diff.length()
            if dist_to_target > 1000:
                self.alpha = 1.0
            else:
                self.alpha = dist_to_target / 1000.0

        else:
            self.visible = False
