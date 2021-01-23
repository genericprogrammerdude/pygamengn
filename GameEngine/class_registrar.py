import sys

from typing import Callable

from game_object_base import GameObjectBase


class ClassRegistrar:
    """Every GameObjectBase child class can register itself with the class registrar to make itself loadable."""

    registry = {}

    @classmethod
    def register(self, name: str) -> Callable:
        """Registers a new GameObject child class."""

        def inner_wrapper(wrapped_class: GameObjectBase) -> Callable:
            if name in self.registry:
                sys.stderr.write("Class '{0}' already registered. Overwriting old value.".format(name))
            self.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper
