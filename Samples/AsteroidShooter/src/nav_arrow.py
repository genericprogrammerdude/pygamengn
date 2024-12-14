from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object import GameObject


@ClassRegistrar.register("NavArrow")
class NavArrow(GameObject):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__gob = None

    @property
    def pointee(self) -> GameObject:
        return self.__gob

    @pointee.setter
    def pointee(self, gob: GameObject):
        """Sets the GameOject to point to."""
        self.__gob = gob

    def update(self, delta):
        super().update(delta)

        if self.__gob and self.parent:
            self.visible = True
            diff = self.__gob.position - self.parent.position
            dist_to_target = diff.length()
            direction = diff / dist_to_target

            self.position = self.parent.position + direction * 150

            _, angle = direction.as_polar()
            self.heading = 270 - angle

            if dist_to_target > 1000:
                self.alpha = 1.0
            else:
                self.alpha = dist_to_target / 1000.0

        else:
            self.visible = False


@ClassRegistrar.register("PowerupArrow")
class PowerupArrow(NavArrow):
    pass
