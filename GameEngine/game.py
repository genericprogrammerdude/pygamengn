import pygame

from collision_manager import CollisionManager
from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Game")
class Game(GameObjectBase):
    """Highest level entity to manage game state."""

    def __init__(self, render_group, collision_manager, updatables, screen):
        self.render_group = render_group
        self.collision_manager = collision_manager
        self.updatables = updatables
        self.screen = screen

    def update(self, delta):
        """Updates the game."""

        # Do collision detection and notification
        self.collision_manager.do_collisions()

        # Update game objects for rendering
        self.render_group.update(self.screen.get_rect(), delta)

        # Render
        self.screen.fill((50, 50, 50))
        self.render_group.draw(self.screen)
        pygame.display.flip()

        self.collision_manager.do_collisions()

        for updatable in self.updatables:
            updatable.update(delta)
