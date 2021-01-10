import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Level")
class Level(GameObjectBase):
    """Abstraction to represent a level to play in."""

    def __init__(self, player_spec, enemy_specs):
        self.player_spec = player_spec
        self.enemy_specs = enemy_specs
        self.player = None
        self.render_group = None

    def create_objects(self, render_group):
        """Creates and initializes the game objects for the level."""
        self.player = GameObjectFactory.create(self.player_spec.game_type)
        self.player.set_pos(pygame.Vector2(self.player_spec.spawn_pos))

        for enemy_spec in self.enemy_specs:
            for spawn_pos in enemy_spec.spawn_pos:
                enemy = GameObjectFactory.create(enemy_spec.game_type)
                enemy.set_pos(pygame.Vector2(spawn_pos))
                enemy.set_target(self.player)

        self.render_group = render_group
        render_group.set_target(self.player)


@GameObjectFactory.register("LevelObject")
class LevelObject(GameObjectBase):
    """Specification for a game object to place in the level."""

    def __init__(self, game_type, spawn_pos):
        self.game_type = game_type
        self.spawn_pos = spawn_pos
