import pygame

from class_registrar import ClassRegistrar
from game_object_base import GameObjectBase


@ClassRegistrar.register("Level")
class Level(GameObjectBase):
    """Abstraction to represent a level to play in."""

    def __init__(self, player_spec, enemy_specs, updatables):
        self.player_spec = player_spec
        self.enemy_specs = enemy_specs
        self.updatables = updatables
        self.player = None
        self.render_group = None

    def create_objects(self, render_group):
        """Creates and initializes the game objects for the level."""
        self.player = self.player_spec.game_type.create()
        self.player.position = pygame.Vector2(self.player_spec.spawn_pos)
        for updatable in self.updatables:
            updatable.set_player(self.player)

        for enemy_spec in self.enemy_specs:
            for spawn_pos in enemy_spec.spawn_pos:
                enemy = enemy_spec.game_type.create()
                enemy.position = pygame.Vector2(spawn_pos)
                enemy.set_target(self.player)

        self.render_group = render_group
        render_group.set_target(self.player)

    def update(self, delta):
        """Updates all the updatables the level owns."""
        for updatable in self.updatables:
            updatable.update(delta)


@ClassRegistrar.register("LevelObject")
class LevelObject(GameObjectBase):
    """Specification for a game object to place in the level."""

    def __init__(self, game_type, spawn_pos):
        self.game_type = game_type
        self.spawn_pos = spawn_pos
