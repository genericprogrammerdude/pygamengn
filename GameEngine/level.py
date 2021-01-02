import pygame

from game_object_factory import GameObjectBase
from game_object_factory import GameObjectFactory


@GameObjectFactory.register("Level")
class Level(GameObjectBase):
    """Abstraction to represent a level to play in."""

    def __init__(self, player_spec, enemy_spec):
        self.player_spec = player_spec
        self.enemy_spec = enemy_spec
        self.player = None
        self.enemies = []

    def create_objects(self, render_group, player_collision_group, enemy_collision_group):
        """Creates and initializes the game objects for the level."""
        self.player = GameObjectFactory.create(self.player_spec.game_type, enemies=enemy_collision_group)
        self.player.set_pos(pygame.Vector2(self.player_spec.spawn_pos))

        for spawn_pos in self.enemy_spec.spawn_pos:
            enemy = GameObjectFactory.create(self.enemy_spec.game_type, enemies=player_collision_group)
            enemy.set_pos(pygame.Vector2(spawn_pos))
            enemy.add_to_groups([render_group, enemy_collision_group])
            self.enemies.append(enemy)

        render_group.set_target(self.player)
        self.player.add_to_groups([render_group, player_collision_group])


@GameObjectFactory.register("LevelObject")
class LevelObject(GameObjectBase):
    """Specification for a game object to place in the level."""

    def __init__(self, game_type, spawn_pos):
        self.game_type = game_type
        self.spawn_pos = spawn_pos
        print(self.game_type, self.spawn_pos)
