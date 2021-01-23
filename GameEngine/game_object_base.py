from _py_abc import ABCMeta


class GameObjectBase(metaclass=ABCMeta):
    """Base class for GameObject."""

    __next_object_id = 0

    def __str__(self):
        return "{0}: {1}".format(self.__object_id, super().__str__())

    def set_object_id(self):
        """
        Sets the object id. This is meant to aid debugging and should only be set once (when GameObjectFactory
        creates the object.
        """
        self.__object_id = GameObjectBase.__next_object_id
        GameObjectBase.__next_object_id += 1

    def get_object_id(self):
        return self.__object_id
