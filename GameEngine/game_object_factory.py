from _py_abc import ABCMeta
# from abc import abstractmethod
from typing import Callable

import pygame


class GameObjectBase(metaclass=ABCMeta):
    """Base class for GameObject."""

#     def __init__(self):
#         """Class constructor."""
#         pass
#
#     @abstractmethod
#     def update(self, delta: int):
#         """Updates the game object."""
#         pass


class GameObjectFactory():
    """GameObject factory."""

    registry = {}
    images = {}
    game_types = {}

    @classmethod
    def initialize(cls):
        cls.images = {
            "ship": pygame.image.load("Assets/SpaceShooterRedux/PNG/playerShip2_blue.png").convert_alpha(),
            "explosion": pygame.image.load("Assets/Explosions/explosion1.png").convert_alpha(),
            "ship": pygame.image.load("Assets/SpaceShooterRedux/PNG/playerShip2_blue.png").convert_alpha(),
            "shield": [
                pygame.image.load("Assets/SpaceShooterRedux/PNG/Effects/shield3.png").convert_alpha(),
                pygame.image.load("Assets/SpaceShooterRedux/PNG/Effects/shield2.png").convert_alpha(),
                pygame.image.load("Assets/SpaceShooterRedux/PNG/Effects/shield1.png").convert_alpha()
            ],
            "turret": pygame.image.load("Assets/SpaceShooterRedux/PNG/Parts/turretBase_big.png").convert_alpha(),
            "turret_gun": pygame.image.load("Assets/SpaceShooterRedux/PNG/Parts/gun04.png").convert_alpha(),
            "projectile": pygame.image.load("Assets/SpaceShooterRedux/PNG/Lasers/laserRed06.png").convert_alpha(),
        }
        cls.game_types = {
            "PlayerShip": {
                "class_name": "Ship",
                "ctor_kwargs": {
                    "image": cls.images["ship"],
                    "velocity_decay_factor": 0.9
                }
            }
        }

    @classmethod
    def create(cls, name: str) -> GameObjectBase:
        """Creates a GameObject instance."""
        try:
            game_type = cls.game_types[name]
            gob_class = cls.registry[game_type["class_name"]]
            gob = gob_class(**game_type["ctor_kwargs"])
            return gob
        except KeyError:
            print("Game type \'%s\' not found.".format(name))
            return None

    @classmethod
    def register(cls, name: str) -> Callable:
        """Registers a new GameObject child class."""

        def inner_wrapper(wrapped_class: GameObjectBase) -> Callable:
            if name in cls.registry:
                print("Class '%s' already registered. Replacing!".format(name))
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper
