import copy
import json
import sys

import pygame

from game_object_base import GameObjectBase
from layer_manager import LayerManager


class GameObjectFactory():
    """
    GameObject factory.

    The following article helped a lot on the details of the implementation of GameObjectFactory:
    https://medium.com/@geoffreykoh/implementing-the-factory-pattern-via-dynamic-registry-and-python-decorators-479fc1537bbe
    """

    class UnknownGameType(Exception):
        """Exception raised when trying to instantiate an unknown GameObject class."""

        def __init__(self, message):
            super().__init__(message)

    def __init__(self, registry, inventory_fp):
        self.layer_manager = None
        self.registry = registry
        data = json.load(inventory_fp)
        inventory_fp.close()

        # Keys that get special treatment
        self.special_keys = [
            ("image:", lambda name, scope: self.images[name]),
            ("sound:", lambda name, scope: self.sounds[name]),
            ("asset:", lambda name, scope: self.assets[name]),
            ("game_object_type:", lambda name, scope: self.create(name, scope)),
            ("type_spec:", lambda name, scope: TypeSpec(self, name))
        ]

        # Initialize game types
        self.game_types = data["game_types"]

        # Load images and sounds, and initialize assets
        self.images = self.__create_assets(data["images"], lambda v: pygame.image.load(v).convert_alpha())
        self.sounds = self.__create_assets(data["sounds"], lambda v: pygame.mixer.Sound(v))
        self.assets = self.__create_assets(data["assets"], lambda v: self.__create_object(v, ""))

        # Build entries for game types that inherit from other types
        self.__build_derived_types()

    def create(self, name: str, scope="", **kwargs) -> GameObjectBase:
        """Creates a GameObject instance."""
        scoped_name = name
        if name[0] != '/':
            scoped_name = "/".join([scope, name])

        game_type = self.__get_game_type(scoped_name)
        gob = self.__create_object(game_type, scoped_name, **kwargs)

        # Add to groups as specified in type spec
        group_names = game_type.get("groups")
        if group_names:
            if isinstance(gob, pygame.sprite.Sprite) and self.layer_manager:
                self.layer_manager.set_layer_id(gob, scoped_name, game_type["class_name"])

            groups = [self.assets[name] for name in group_names]
            gob.add_to_groups(groups)

        # Create attachments
        attachment_specs = game_type.get("attachments")
        if gob and attachment_specs:
            for attachment_spec in attachment_specs:
                attachment_object = self.create(attachment_spec["game_type"], scoped_name)
                if attachment_object:
                    parent_transform = attachment_spec.get("parent_transform")
                    if parent_transform == None:
                        parent_transform = True
                    gob.attach(attachment_object, attachment_spec["offset"], parent_transform)
                    gob.transform()

        return gob

    def set_layer_manager_asset_name(self, name):
        """Sets the layer manager asset name for the factory to automatically assign layers to GameObjects."""
        layer_manager_spec = self.assets.get(name)
        if layer_manager_spec:
            self.layer_manager = layer_manager_spec
        else:
            sys.stderr.write("GameObjectFactory: LayerManager '{0}' not in inventory assets.\n".format(name))

    def __get_game_type(self, name: str) -> dict:
        """Gets the given game type, recursing into nested dictionaries as necessary."""
        keys = name.lstrip('/').split('/')
        game_type = self.game_types
        while len(keys) > 0:
            try:
                for key in keys:
                    game_type = game_type[key]
                return game_type
            except KeyError:
                del keys[0]
                game_type = self.game_types
        raise GameObjectFactory.UnknownGameType("".join(["Unknown game type: ", name]))

    def __resolve_refs(self, attribute_key, attribute_value, special_key, resolved_refs, scope):
        """Resolves references."""
        # Get the name of the key to populate in resolved_refs
        key = attribute_key[len(special_key[0]):]

        if isinstance(attribute_value, str):
            # Simple string value -> assign it to resolved_refs
            resolved_refs[key] = special_key[1](attribute_value, scope)  # self_dict[attribute_value]

        elif isinstance(attribute_value, list):
            # The value is a list -> recurse and assign
            resolved_refs[key] = []
            self.__assign_asset_list(attribute_value, resolved_refs[key], special_key[1], scope)
        else:
            sys.stderr.write("GameObjectFactory.__resolve_refs(): Unrecognized type '{0}' for key '{1}'\n".format(
                type(attribute_value),
                attribute_key
            ))

    def __create_object(self, type_spec, scope, **kwargs) -> GameObjectBase:
        """Creates and returns a GameObjectBase instance from the given type specification."""
        resolved_refs = {}
        type_spec_kwargs = type_spec["kwargs"]
        for key in type_spec_kwargs:
            is_special_key = False

            for special_key in self.special_keys:
                if key.startswith(special_key[0]):
                    is_special_key = True
                    self.__resolve_refs(key, type_spec_kwargs[key], special_key, resolved_refs, scope)

            if not is_special_key:
                resolved_refs[key] = type_spec_kwargs[key]

        try:
            gob_class = self.registry[type_spec["class_name"]]
            gob = gob_class(**resolved_refs, **kwargs)
            return gob
        except KeyError:
            sys.stderr.write("GameObjectBase subclass '{0}' not found.\n".format(type_spec["class_name"]))
            return None

    def __assign_asset_list(self, asset_names, asset_list, asset_retriever, scope):
        """
        Goes into asset_list and assigns the initialized assets to the right asset spec elements in the assets
        dictionary. This enables support for nested lists of assets in the asset specs. See the CollisionManager
        for an example of a GameObject that relies on this.
        """
        for asset_name in asset_names:
            if isinstance(asset_name, str):
                asset_list.append(asset_retriever(asset_name, scope))
            else:
                asset_list.append([])
                self.__assign_asset_list(asset_name, asset_list[-1], asset_retriever, scope)

    def __create_assets(self, dictionary, creator_func):
        """Creates a dictionary of loaded and initialized assets using the creator_func."""
        rv = {}
        for key, value in dictionary.items():
            rv[key] = creator_func(value)
        return rv

    def __build_derived_types(self):
        """Builds entries in game_types that are for types that derived from other types."""
        for key in list(self.game_types.keys()):
            key_parts = key.split(':')
            if len(key_parts) == 2:
                child_type = key_parts[0]
                parent_type = key_parts[1]
                if not child_type in self.game_types and parent_type in self.game_types:
                    self.game_types[child_type] = copy.deepcopy(self.game_types[parent_type])
                    for child_key in self.game_types[key]:
                        self.__recursive_copy(self.game_types[key], self.game_types[child_type], child_key)
                    del self.game_types[key]

                else:
                    sys.stderr.write("Derived type '{0}' already exists or parent '{1}' not found.\n".format(
                        child_type, parent_type
                    ))

    def __recursive_copy(self, from_obj, to_obj, key):
        """Recursively copies dictionary keys."""
        if isinstance(from_obj[key], dict):
            for subkey in from_obj[key]:
                self.__recursive_copy(from_obj[key], to_obj[key], subkey)
        elif isinstance(from_obj[key], list):
            to_obj[key] = copy.deepcopy(from_obj[key])
        else:
            to_obj[key] = from_obj[key]


class TypeSpec:
    """GameObject constructor for objects that create objects at runtime."""

    def __init__(self, factory, spec):
        self.factory = factory
        self.spec = spec

    def create(self, **kwargs):
        """Creates an instance from the spec."""
        return self.factory.create(self.spec, **kwargs)
