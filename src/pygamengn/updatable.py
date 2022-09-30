import abc

from pygamengn.game_object_base import GameObjectBase


class Updatable(GameObjectBase):
    """Base class for objects that the Game object will update and pass some information to."""

    @abc.abstractmethod
    def update(self, delta):
        pass

    @abc.abstractmethod
    def set_player(self, player):
        pass
