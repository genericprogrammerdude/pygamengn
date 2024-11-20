from enum import Enum, auto

import pygame
import pygamengn

from main_menu import MainMenu


@pygamengn.ClassRegistrar.register("UISample")
class UISample(pygamengn.Game):

    def __init__(
            self,
            main_menu_ui,
            **kwargs
        ):
        super().__init__(**kwargs)
        self.main_menu_ui = main_menu_ui
        self.main_menu_ui.set_exit_callback(self.exit_game)
        self.show_ui(self.main_menu_ui, 500)
