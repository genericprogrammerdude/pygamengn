import pygame

from collision_manager import CollisionManager
from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Game")
class Game(GameObjectBase):
    """Highest level entity to manage game state."""

    def __init__(self, render_group, collision_manager, screen):
        self.render_group = render_group
        self.collision_manager = collision_manager
        self.screen = screen
        self.is_paused = False
        self.blit_surfaces = []
        self.player = None

    def update(self, delta):
        """Updates the game."""

        if self.is_paused:
            delta = 0

        # Do collision detection and notification
        self.collision_manager.do_collisions()

        # Update game objects for rendering
        self.render_group.update(self.screen.get_rect(), delta)

        # Render
        self.screen.fill((50, 50, 50))
        self.render_group.draw(self.screen)
        for blit_surface in self.blit_surfaces:
            self.screen.blit(blit_surface.surface, blit_surface.topleft)
        pygame.display.flip()

        self.blit_surfaces.clear()

        self.collision_manager.do_collisions()

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


class BlitSurface:
    """Specification for a surface that will be blitted while rendering."""

    def __init__(self, surface, topleft):
        """topleft is in screen coordinates."""
        self.surface = surface
        self.topleft = topleft
