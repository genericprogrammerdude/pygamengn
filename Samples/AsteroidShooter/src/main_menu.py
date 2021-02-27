import pygame

from UI.font_asset import FontAsset
from UI.panel import ColourPanel
from asteroid import AsteroidSpawner
from class_registrar import ClassRegistrar


@ClassRegistrar.register("MainMenu")
class MainMenu(ColourPanel):
    """Main menu UI."""

    def __init__(self, asteroid_spawner, **kwargs):
        super().__init__(**kwargs)
        self.bind_children()
        self.asteroid_spawner = asteroid_spawner
        self.start_callback = None
        self.exit_callback = None
        self.multiplyaer_callback = None

    def update(self, parent_rect, delta):
        """Updates the main menu."""
        super().update(parent_rect, delta)
        self.handle_input()
        self.asteroid_spawner.update(delta)

    def handle_input(self):
        """Reads and handles input."""
        mouse_pos = pygame.mouse.get_pos()
        self.propagate_mouse_pos(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.exit_callback()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.start_button.rect.collidepoint(mouse_pos):
                    self.start_callback()
                elif self.exit_button.rect.collidepoint(mouse_pos):
                    self.exit_callback()

    def set_start_callback(self, start_callback):
        """Sets the function to call when the start button is clicked."""
        self.start_callback = start_callback

    def set_exit_callback(self, exit_callback):
        """Sets the function to call when the exit button is clicked."""
        self.exit_callback = exit_callback
