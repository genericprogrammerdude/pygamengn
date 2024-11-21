from abc import abstractmethod

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase



@ClassRegistrar.register("InputHandler")
class InputHandler(GameObjectBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Processes the given event and returns True if it handled it, False otherwise."""
        pass


@ClassRegistrar.register("DefaultInputHandler")
class DefaultInputHandler(InputHandler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Processes the given event and returns True if it handled it, False otherwise."""
        rv = False
        if event.type == pygame.QUIT:
            self.exit_game()
            rv = True
        elif event.type == pygame.VIDEORESIZE:
            self.resize_window(pygame.Rect(0, 0, event.w, event.h))
            rv = True
        return rv

    @abstractmethod
    def exit_game(self):
        pass

    @abstractmethod
    def resize_window(self, rect: pygame.Rect):
        pass
