import pygame

from collision_manager import CollisionManager
from font_asset import FontAsset
from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Game")
class Game(GameObjectBase):
    """Highest level entity to manage game state."""

    def __init__(self, render_group, collision_manager, updatables, screen, font, text_colour):
        self.render_group = render_group
        self.collision_manager = collision_manager
        self.updatables = updatables
        self.screen = screen
        self.is_paused = False
        self.font = font
        self.time = 0
        self.text_colour = text_colour
        self.score = 0
        self.player = None

        # Assign biggest rectangle for time text
        s = "00:00"
        surface = self.font.font.render(s, True, self.text_colour)
        self.time_text_width = surface.get_rect().width
        s = "0000"
        surface = self.font.font.render(s, True, self.text_colour)
        self.score_text_width = surface.get_rect().width

    def update(self, delta):
        """Updates the game."""

        if self.is_paused:
            delta = 0

        if not self.player is None and self.player.alive():
            self.time += delta
            self.score = self.player.score

        # Do collision detection and notification
        self.collision_manager.do_collisions()

        # Update game objects for rendering
        self.render_group.update(self.screen.get_rect(), delta)

        # Put text together
        time_surface = self.build_time_text_surface()
        score_surface = self.build_score_text_surface()

        # Render
        self.screen.fill((50, 50, 50))
        self.render_group.draw(self.screen)
        self.screen.blit(time_surface, (self.screen.get_rect().width - self.time_text_width, 0))
        self.screen.blit(score_surface, (self.score_text_width - score_surface.get_rect().width, 0))
        pygame.display.flip()

        self.collision_manager.do_collisions()

        for updatable in self.updatables:
            updatable.update(delta)

    def set_player(self, player):
        """Tells the updateables which game object is the player."""
        self.player = player
        for updatable in self.updatables:
            updatable.set_player(player)

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def build_time_text_surface(self):
        total_sec = self.time // 1000
        sec = total_sec % 60
        min = total_sec // 60
        surface = self.font.font.render("{:02d}:{:02d}".format(min, sec), True, self.text_colour)
        return surface

    def build_score_text_surface(self):
        surface = self.font.font.render("{:03d}".format(self.score), True, self.text_colour)
        return surface
