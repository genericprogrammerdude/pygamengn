from abc import abstractmethod

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase



@ClassRegistrar.register("InputHandler")
class InputHandler(GameObjectBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def handle_event(self, event: pygame.event) -> bool:
        """Processes the given event and returns True if it handled it, False otherwise."""
        pass


@ClassRegistrar.register("DefaultInputHandler")
class DefaultInputHandler(InputHandler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def handle_event(self, event: pygame.event) -> bool:
        """Processes the given event and returns True if it handled it, False otherwise."""
        rv = False
        if event.type == pygame.QUIT:
            self.exit_game()
            rv = True
        return rv

    @abstractmethod
    def exit_game(self):
        pass