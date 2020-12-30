from _py_abc import ABCMeta
import sys
from typing import Callable

import pygame


class GameObjectBase(metaclass=ABCMeta):
    """Base class for GameObject."""


class GameObjectFactory():
    """
    GameObject factory.

    The following article helped a lot on the details of the implementation of GameObjectFactory:
    https://medium.com/@geoffreykoh/implementing-the-factory-pattern-via-dynamic-registry-and-python-decorators-479fc1537bbe
    """

    registry = {}
    images = {}
    game_types = {}
    assets = {}

    @classmethod
    def initialize(cls):
        load = pygame.image.load
        cls.images = {
            "ship": load("Assets/SpaceShooterRedux/PNG/playerShip2_blue.png").convert_alpha(),
            "explosion": load("Assets/Explosions/explosion1.png").convert_alpha(),
            "ship": load("Assets/SpaceShooterRedux/PNG/playerShip2_blue.png").convert_alpha(),
            "shield": [
                load("Assets/SpaceShooterRedux/PNG/Effects/shield3.png").convert_alpha(),
                load("Assets/SpaceShooterRedux/PNG/Effects/shield2.png").convert_alpha(),
                load("Assets/SpaceShooterRedux/PNG/Effects/shield1.png").convert_alpha()
            ],
            "turret": load("Assets/SpaceShooterRedux/PNG/Parts/turretBase_big.png").convert_alpha(),
            "turret_gun": load("Assets/SpaceShooterRedux/PNG/Parts/gun04.png").convert_alpha(),
            "turret_projectile": load("Assets/SpaceShooterRedux/PNG/Lasers/laserRed06.png").convert_alpha(),
        }

        cls.assets = {
            "explosion_atlas": {
                "class_name": "Atlas",
                "kwargs": {
                    "image": cls.images["explosion"],
                    "frame_size": (256, 256)
                },
                "asset": None
            }
        }
        for key in cls.assets.keys():
            asset_spec = cls.assets[key]
            asset_spec["asset"] = GameObjectFactory.create_object(asset_spec)

        cls.game_types = {
            "PlayerShip": {
                "class_name": "Ship",
                "kwargs": {
                    "image": cls.images["ship"],
                    "velocity_decay_factor": 0.9
                }
            },
            "EnemyTurret": {
                "class_name": "Turret",
                "kwargs": {
                    "image": cls.images["turret"],
                    "projectile_type": "EnemyTurretProjectile"
                }
            },
            "EnemyTurretProjectile": {
                "class_name": "Projectile",
                "kwargs": {
                    "image": cls.images["turret_projectile"],
                    "death_effect": "Explosion",
                    "damage": 10
                }
            },
            "Explosion": {
                "class_name": "AnimatedTexture",
                "kwargs": {
                    "atlas": cls.assets["explosion_atlas"]["asset"],
                    "duration": 750
                }
            }
        }

    @classmethod
    def create(cls, name: str, **kwargs) -> GameObjectBase:
        """Creates a GameObject instance."""
        try:
            game_type = cls.game_types[name]
        except KeyError:
            sys.stderr.write("Game type '{0}' not found.\n".format(name))
            return None

        return GameObjectFactory.create_object(game_type, **kwargs)

    @classmethod
    def create_object(cls, type_spec, **kwargs):
        try:
            gob_class = cls.registry[type_spec["class_name"]]
            gob = gob_class(**type_spec["kwargs"], **kwargs)
            return gob
        except KeyError:
            sys.stderr.write("GameObjectBase child class '{0}' not found.\n".format(type_spec["class_name"]))
            return None

    @classmethod
    def register(cls, name: str) -> Callable:
        """Registers a new GameObject child class."""

        def inner_wrapper(wrapped_class: GameObjectBase) -> Callable:
            if name in cls.registry:
                sys.stderr.write("Class '{0}' already registered. Overwriting old value.".format(name))
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper
