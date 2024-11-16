import pygame

from pygamengn.blit_surface import BlitSurface
from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase
from pygamengn.UI.root import Root


@ClassRegistrar.register("Game")
class Game(GameObjectBase):
    """Highest level entity to manage game state."""

    def __init__(self, render_group, collision_manager, screen, replication_manager=None):
        self.render_group = render_group
        self.collision_manager = collision_manager
        self.replication_manager = replication_manager
        self.screen = screen
        self.is_paused = False
        self.blit_surfaces = []
        self.player = None
        self._uis = []

    def update(self, delta):
        """Updates the game."""

        if self.is_paused:
            delta = 0

        # Update game objects for rendering
        self.render_group.update(self.screen.get_rect(), delta)

        # Do collision detection and notification
        self.collision_manager.do_collisions()

        # Do data replication as appropriate
        if self.replication_manager:
            self.replication_manager.update(delta)

        # Update any active UI screens
        i = 0
        while i < len(self._uis):
            if not self._uis[i].update(self.screen.get_rect(), delta):
                self._uis.pop(i)
            else:
                i += 1

        # Render
        self.render_group.draw(self.screen)
        self.direct_draw()
        for blit_surface in self.blit_surfaces:
            self.screen.blit(blit_surface.surface, blit_surface.topleft)
        for ui in self._uis:
            ui.blit_to_surface(self.screen)
        pygame.display.flip()

        self.blit_surfaces.clear()

    def set_player(self, player):
        """Tells the updateables which game object is the player."""
        self.player = player
        self.player.die_callback(self.handle_player_death)

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def add_blit_surface(self, blit_surface):
        """Adds a surface to blit when rendering. The list gets cleared after every game update."""
        self.blit_surfaces.append(blit_surface)

    def handle_player_death(self):
        """Invoked when the player dies."""
        pass

    def direct_draw(self):
        """Invoked after drawing render_group to the screen. Implement this for any direct-drawing needs."""
        pass

    def show_ui(self, ui: Root, fade_in_ms: int):
        """
        Shows the specified ui, fading it into the screen during fade_in number of ms.

        After a UI Root is shown, its update() method will be invoked as part of Game's update loop until the UI
        is hidden.
        """
        if ui not in self._uis:
            self._uis.append(ui)
        ui.fade_in(fade_in_ms)

    def hide_ui(self, ui: Root, fade_out_ms: int):
        """Hides the specified ui, fading it into the screen during fade_in number of ms."""
        if ui in self._uis:
            ui.fade_in(fade_in_ms)

    def blit_ui(self, ui):
        self.add_blit_surface(ui.root_blit_surface)
