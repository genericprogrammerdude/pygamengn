import pygame

from pygamengn.blit_surface import BlitSurface
from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase
from pygamengn.UI.root import Root


@ClassRegistrar.register("Game")
class Game(GameObjectBase):
    """Highest level entity to manage game state."""

    def __init__(self, render_group, collision_manager, screen, replication_manager=None):
        self._render_group = render_group
        self._collision_manager = collision_manager
        self._replication_manager = replication_manager
        self._screen = screen
        self._is_paused = False
        self._blit_surfaces = []
        self._player = None
        self._uis = []

    def update(self, delta):
        """Updates the game."""

        if self._is_paused:
            real_delta = delta
            delta = 0

        # Update game objects for rendering
        self._render_group.update(self._screen.get_rect(), delta)

        # Do collision detection and notification
        self._collision_manager.do_collisions()

        # Do data replication as appropriate
        if self._replication_manager:
            self._replication_manager.update(delta)

        # Update any active UI screens
        i = 0
        while i < len(self._uis):
            if not self._uis[i].update(real_delta if self._is_paused and self._uis[i].update_on_pause else delta):
                self._uis.pop(i)
            else:
                i += 1

        # Render
        self._render_group.draw(self._screen)
        self.direct_draw()
        for blit_surface in self._blit_surfaces:
            self._screen.blit(blit_surface.surface, blit_surface.topleft)
        for ui in self._uis:
            ui.blit_to_surface(self._screen)
        pygame.display.flip()

        self._blit_surfaces.clear()

    def set_player(self, player):
        """Tells the updateables which game object is the player."""
        self._player = player
        self._player.die_callback(self.handle_player_death)

    def toggle_pause(self):
        self._is_paused = not self._is_paused

    def add_blit_surface(self, blit_surface):
        """Adds a surface to blit when rendering. The list gets cleared after every game update."""
        self._blit_surfaces.append(blit_surface)

    def handle_player_death(self):
        """Invoked when the player dies."""
        pass

    def direct_draw(self):
        """Invoked after drawing render_group to the screen. Implement this for any direct-drawing needs."""
        pass

    def show_ui(self, ui: Root, fade_in_ms: int = 0):
        """
        Shows the specified ui, fading it into the screen during fade_in_ms number of ms.

        After a UI Root is shown, its update() method will be invoked as part of Game's update loop until the UI
        is hidden.
        """
        if ui not in self._uis:
            self._uis.append(ui)
        ui.set_parent_rect(self._screen.get_rect())
        ui.fade_in(fade_in_ms)

    def hide_ui(self, ui: Root, fade_out_ms: int = 0):
        """Hides the specified ui, fading it into the screen during fade_in_ms number of ms."""
        if ui in self._uis:
            ui.fade_out(fade_out_ms)

    def toggle_ui(self, ui: Root, fade_ms: int = 0) -> bool:
        """Shows or hides a UI, depending on whether it's currently being shown."""
        if ui in self._uis:
            self.hide_ui(ui, fade_ms)
            return False
        else:
            self.show_ui(ui, fade_ms)
            return True

    def blit_ui(self, ui):
        self.add_blit_surface(ui.root_blit_surface)
