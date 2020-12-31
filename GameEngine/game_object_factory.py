from _py_abc import ABCMeta
import json
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
    surfaces = {}
    game_types = {}
    assets = {}
    __image_json_objects = []
    __asset_json_objects = []

    @classmethod
    def initialize(cls, inventory_fp):
        data = json.load(inventory_fp, object_hook=GameObjectFactory.__json_object_hook)

        # Load surfaces
        cls.surfaces = {}
        data_images = data["surfaces"]
        for key in data_images.keys():
            cls.surfaces[key] = pygame.image.load(data_images[key])

        # Assets and game_types can be assigned directly
        cls.game_types = data["game_types"]

        # Initialize assets with surfaces and the corresponding asset object
        cls.assets = data["assets"]
        for key in cls.assets.keys():
            asset_spec = cls.assets[key]
            if isinstance(asset_spec["kwargs"]["image"], str):
                asset_spec["kwargs"]["image"] = cls.surfaces[asset_spec["kwargs"]["image"]]
            elif isinstance(asset_spec["kwargs"]["image"], list):
                images = asset_spec["kwargs"]["image"]
                asset_spec["kwargs"]["image"] = cls.surfaces[images[0]]
                asset_spec["kwargs"]["images"] = [cls.surfaces[images[i]] for i in range(len(images))]
            asset_spec["asset"] = GameObjectFactory.__create_object(asset_spec)

        # Replace image names with loaded Surfaces
        for o in cls.__image_json_objects:
            if isinstance(o["image"], str):
                image_str = o["image"]
                o["image"] = cls.surfaces[image_str]
            elif isinstance(o["image"], list):
                images = o["image"]
                o["image"] = cls.surfaces[images[0]]
                o["images"] = [cls.surfaces[images[i]] for i in range(len(images))]
        del cls.__image_json_objects

        # Replace asset names with the loaded assets
        for o in cls.__asset_json_objects:
            if isinstance(o["asset"], str):
                asset_str = o["asset"]
                o["asset"] = cls.assets[asset_str]["asset"]
        del cls.__asset_json_objects

    @classmethod
    def create(cls, name: str, **kwargs) -> GameObjectBase:
        """Creates a GameObject instance."""
        try:
            game_type = cls.game_types[name]
        except KeyError:
            sys.stderr.write("Game type '{0}' not found.\n".format(name))
            return None

        gob = GameObjectFactory.__create_object(game_type, **kwargs)

        attachment_specs = game_type.get("attachments")
        if gob and attachment_specs:
            for attachment_spec in attachment_specs:
                attachment_object = GameObjectFactory.create(attachment_spec["game_type"])
                if attachment_object:
                    parent_transform = attachment_spec.get("parent_transform")
                    if parent_transform == None:
                        parent_transform = True
                    gob.attach(attachment_object, attachment_spec["offset"], parent_transform)

        return gob

    @classmethod
    def __create_object(cls, type_spec, **kwargs) -> GameObjectBase:
        try:
            gob_class = cls.registry[type_spec["class_name"]]
            gob = gob_class(**type_spec["kwargs"], **kwargs)
            return gob
        except KeyError:
            sys.stderr.write("GameObjectBase child class '{0}' not found.\n".format(type_spec["class_name"]))
            return None

    @classmethod
    def __json_object_hook(cls, obj_dict):
        """Keeps track of JSON objects (dictionaries) that will have to be initialized further."""
        if "image" in obj_dict:
            cls.__image_json_objects.append(obj_dict)
        if "asset" in obj_dict:
            cls.__asset_json_objects.append(obj_dict)
        return obj_dict

    @classmethod
    def register(cls, name: str) -> Callable:
        """Registers a new GameObject child class."""

        def inner_wrapper(wrapped_class: GameObjectBase) -> Callable:
            if name in cls.registry:
                sys.stderr.write("Class '{0}' already registered. Overwriting old value.".format(name))
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper
