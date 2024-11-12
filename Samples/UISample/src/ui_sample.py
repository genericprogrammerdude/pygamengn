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

    def update(self, delta):
        """Updates the game."""

        if self.mode == Mode.MAIN_MENU:
            self.update_ui(delta, self.main_menu_ui)

        elif self.mode == Mode.PAUSE_MENU:
            self.update_ui(delta, self.pause_menu_ui)

        elif self.mode == Mode.DEBRIEF:
            self.update_ui(delta, self.debrief_panel)

        super().update(delta)

    def update_ui(self, delta, ui):
        """Updates the given UI component."""
        pygame.mouse.set_visible(True)
        ui.update(self.screen.get_rect(), delta)
        self.blit_ui(ui)

    def exit_game(self):
        """Exits the application."""
        self.running = False

    def go_to_main_menu(self):
        """Goes back to the main menu after showing the debrief UI."""
        self.mode = Mode.MAIN_MENU

    def handle_input(self):
        """Reads input and makes things happen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle_pause()
                    self.mode = Mode.PAUSE_MENU
