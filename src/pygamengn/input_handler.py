from abc import abstractmethod

import pygame

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase



@ClassRegistrar.register("InputHandler")
class InputHandler(GameObjectBase):

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Processes the given event and returns True if it handled it, False otherwise."""
        pass

    def activate(self) -> bool:
        """This is invoked when the input handler becomes active."""
        pass

    def deactivate(self) -> bool:
        """This is invoked when the input handler is deactivated."""
        pass


@ClassRegistrar.register("DefaultInputHandler")
class DefaultInputHandler(InputHandler):

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Processes the given event and returns True if it handled it, False otherwise."""
        rv = False
        if event.type == pygame.QUIT:
            self.exit_game()
            rv = True
        elif event.type == pygame.VIDEORESIZE:
            self.resize_window(pygame.Rect(0, 0, event.w, event.h))
            rv = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKQUOTE:
                self.toggle_console()
                rv = True
        return rv

    @abstractmethod
    def exit_game(self):
        pass

    @abstractmethod
    def resize_window(self, rect: pygame.Rect):
        pass

    def toggle_console(self):
        """Subclasses can implement this method to show or hide the game console."""
        pass
