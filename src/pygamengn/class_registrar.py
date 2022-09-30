import logging

from typing import Callable

from pygamengn.game_object_base import GameObjectBase


class ClassRegistrar:
    """
    Every GameObjectBase child class can register itself with the class registrar to make itself loadable.

    The following article helped a lot on the details of the implementation of GameObjectFactory:
    https://medium.com/@geoffreykoh/implementing-the-factory-pattern-via-dynamic-registry-and-python-decorators-479fc1537bbe
    """

    registry = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        """Registers a new GameObject child class."""

        def inner_wrapper(wrapped_class: GameObjectBase) -> Callable:
            if name in cls.registry:
                logging.warn("Class '{0}' already registered; overwriting old value".format(name))
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper
