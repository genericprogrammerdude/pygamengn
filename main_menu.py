import pygame

from UI.font_asset import FontAsset
from UI.panel import ColourPanel
from asteroid import AsteroidSpawner
from game import Game
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("MainMenu")
class MainMenu(ColourPanel):
    """Main menu UI."""

    def __init__(self, asteroid_spawner, **kwargs):
        super().__init__(**kwargs)
        self.asteroid_spawner = asteroid_spawner
        self.start_button = self.children[0]
        self.exit_button = self.children[1]
        self.start_callback = None
        self.exit_callback = None

    def update(self, parent_rect, delta):
        """Updates the main menu."""
        self.handle_input()
        super().update(parent_rect, delta)
        self.asteroid_spawner.update(delta)

    def handle_input(self):
        """Reads and handles input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.exit_callback()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start_callback()

    def click_start(self):
        """Starts a new game."""
        pass

    def click_exit(self):
        """Exits the application."""
        pass

    def set_start_callback(self, start_callback):
        """Sets the function to call when the start button is clicked."""
        self.start_callback = start_callback

    def set_exit_callback(self, exit_callback):
        """Sets the function to call when the exit button is clicked."""
        self.exit_callback = exit_callback
