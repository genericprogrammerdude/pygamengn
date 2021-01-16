import pygame

from UI.font_asset import FontAsset
from UI.panel import ColourPanel
from game import Game
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("MainMenu")
class MainMenu(ColourPanel):
    """Main menu UI."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_button = self.children[0]
        self.exit_button = self.children[1]
        self.game = None

    def set_game(self, game):
        """Sets the instance of Game to interact with."""
        self.game = game

    def click_start(self):
        """Starts a new game."""
        pass

    def click_exit(self):
        """Exits the application."""
        self.game.running = False
