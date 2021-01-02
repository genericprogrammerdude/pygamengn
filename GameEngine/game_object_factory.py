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
    layer_manager = None

    __asset_json_objects = []
    __asset_list_json_objects = []

    @classmethod
    def initialize(cls, inventory_fp):
        data = json.load(inventory_fp, object_hook=GameObjectFactory.__json_object_hook)

        # Load surfaces
        cls.surfaces = {}
        data_images = data["surfaces"]
        for key in data_images.keys():
            cls.surfaces[key] = pygame.image.load(data_images[key]).convert_alpha()

        # Assets and game_types can be assigned directly
        cls.game_types = data["game_types"]

        # Initialize assets with surfaces and the corresponding asset object
        cls.assets = data["assets"]

        # Create asset objects
        for key in cls.assets.keys():
            asset_spec = cls.assets[key]
            asset_spec["asset"] = GameObjectFactory.__create_object(asset_spec)

        # Assign initialized assets to the fields that reference them
        for obj, key in cls.__asset_json_objects:
            asset_name = obj[key]
            obj[key[len("asset:"):]] = cls.assets[asset_name]["asset"]
            del obj[key]
        del cls.__asset_json_objects

        # Assign initialized assets to the fields that reference asset lists
        # TODO: Implement me!
        del cls.__asset_list_json_objects

        # Initialize layer manager if there is one
        cls.layer_manager = cls.create("LayerManager")

    @classmethod
    def create(cls, name: str, **kwargs) -> GameObjectBase:
        """Creates a GameObject instance."""
        try:
            game_type = GameObjectFactory.__get_game_type(name)
        except KeyError:
            sys.stderr.write("Game type '{0}' not found.\n".format(name))
            return None

        # Get layer id for the GameObject
        layer_id = LayerManager.invalid_layer_id
        if cls.layer_manager != None:
            layer_id = cls.layer_manager.get_layer_id(name)
            if layer_id == cls.layer_manager.invalid_layer_id:
                layer_id = cls.layer_manager.get_layer_id(game_type["class_name"])

        # name not found in known layers
#         if layer_id == LayerManager.invalid_layer_id:
#             sys.stderr.write("Game type name '{0}' doesn't have an assigned layer in LayerManager.\n".format(
#                 name
#             ))

        gob = GameObjectFactory.__create_object(game_type, **kwargs)
        if layer_id != LayerManager.invalid_layer_id:
            gob.set_layer_id(layer_id)

        # Create attachments
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
    def __get_game_type(cls, name: str) -> dict:
        """Gets the given game type, recursing into nested dictionaries as necessary."""
        #
        # TODO: Given game type A that references game type B, search for B in the "local context" first (i.e., search
        # for B going up the hierarchy of dictionaries). This will remove the need to provide full context for
        # referencing B from A. Instead of referencing "/CommonParent/B", A could reference "B" and that should be
        # enough to find "/CommonParent/B" from A.
        #
        keys = name.split('/')
        game_type = cls.game_types
        for key in keys:
            game_type = game_type[key]
        return game_type

    @classmethod
    def __create_object(cls, type_spec, **kwargs) -> GameObjectBase:
        # Assemble new game type dictionary with resolved "image:", "image_list:", and "game_object_type:" fields
        resolved_refs = {}
        type_spec_kwargs = type_spec["kwargs"]
        for key in type_spec_kwargs:
            if key.startswith("image:"):
                image_name = type_spec_kwargs[key]
                resolved_refs[key[len("image:"):]] = cls.surfaces[image_name]
            elif key.startswith("image_list:"):
                image_list = type_spec_kwargs[key]
                resolved_refs[key[len("image_list:"):]] = [cls.surfaces[image_str] for image_str in image_list]
            elif key.startswith("asset:"):
                print("Found asset:", key, type_spec_kwargs[key])
            elif key.startswith("game_object_type:"):
                gob_type_name = type_spec_kwargs[key]
                resolved_refs[key[len("type_spec_object:"):]] = GameObjectFactory.create(gob_type_name)
            else:
                resolved_refs[key] = type_spec_kwargs[key]

        try:
            gob_class = cls.registry[type_spec["class_name"]]
            gob = gob_class(**resolved_refs, **kwargs)
            return gob
        except KeyError:
            sys.stderr.write("GameObjectBase subclass '{0}' not found.\n".format(type_spec["class_name"]))
            return None

    @classmethod
    def __json_object_hook(cls, obj_dict):
        """Keeps track of JSON objects (dictionaries) that will have to be initialized further."""
        for key in obj_dict.keys():
            if key.startswith("asset:"):
                cls.__asset_json_objects.append((obj_dict, key))
            elif key.startswith("asset_list:"):
                cls.__asset_list_json_objects.append((obj_dict, key))
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


@GameObjectFactory.register("LayerManager")
class LayerManager():
    """
    Manages draw layers semi-automatically.

    The order of GameObject subclasses defined in self.layers determines the draw order. Abstract game types
    declared in the inventory file can also be used in self.layers.

    GameObjectFactory sets the 'layer' constructor argument in every GameObject instance it creates. The value of
    the parameter comes from the object's class or abstract game type, as defined in LayerManager's 'layers' list.
    """

    invalid_layer_id = -1

    def __init__(self, layers):
        self.layers = layers

    def get_layer_id(self, name):
        """Returns the layer for the given game type name."""
        for index, layer in enumerate(self.layers):
            if name in layer:
                return index
        return self.invalid_layer_id
