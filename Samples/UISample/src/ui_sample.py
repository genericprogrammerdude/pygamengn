from enum import Enum, auto

import pygame
import pygamengn

from debrief_panel import DebriefPanel
from main_menu import MainMenu
from pause_menu import PauseMenu


class Mode(Enum):
    """The mode of the AsteroidShooterGame defines game behaviour."""
    MAIN_MENU = auto()
    PAUSE_MENU = auto()
    DEBRIEF = auto()


@pygamengn.ClassRegistrar.register("UISample")
class UISample(pygamengn.Game):

    def __init__(
            self,
            main_menu_ui,
            # pause_menu_ui,
            # debrief_panel,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.main_menu_ui = main_menu_ui
        # self.pause_menu_ui = pause_menu_ui
        # self.debrief_panel = debrief_panel
        self.running = True
        self.mode = Mode.MAIN_MENU
        self.main_menu_ui.set_exit_callback(self.exit_game)
        self.show_ui(self.main_menu_ui, 500)

    def exit_game(self):
        """Exits the application."""
        self.running = False

    def handle_input(self):
        """Reads input and makes things happen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle_pause()
                    self.mode = Mode.PAUSE_MENU
