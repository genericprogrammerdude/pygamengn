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

        # Initialize game types
        self.game_types = data["game_types"]

        # Load images and sounds, and initialize assets
        self.images = self.__create_assets(data["images"], lambda v: pygame.image.load(v).convert_alpha())
        self.sounds = self.__create_assets(data["sounds"], lambda v: pygame.mixer.Sound(v))
        self.assets = self.__create_assets(data["assets"], lambda v: self.__create_object(v, ""))

        # Keys that get special treatment
        self.special_keys = [
            ("image:", lambda name: self.images[name]),
            ("sound:", lambda name: self.sounds[name]),
            ("asset:", lambda name: self.assets[name]),
            ("game_object_type:", lambda name, scope: self.create(name, scope)),
            ("type_spec:", lambda name: TypeSpec(self, name))
        ]

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

#     def __resolve_refs(self, name, resolved_refs, retriever_func):
#         """Resolves references."""

    def __create_object(self, type_spec, scope, **kwargs) -> GameObjectBase:
        """Creates and returns a GameObjectBase instance from the given type specification."""
        resolved_refs = {}
        type_spec_kwargs = type_spec["kwargs"]
        for key in type_spec_kwargs:

#             for special_key, object_retriever in self.special_keys:
#                 if key.startswith(special_key):
#                     resolved_refs = self.__resolve_refs(type_spec_kwargs[key], object_retriever)

            if key.startswith("image:"):
                image_name = type_spec_kwargs[key]
                if isinstance(image_name, str):
                    resolved_refs[key[len("image:"):]] = self.images[image_name]
                elif isinstance(image_name, list):
                    image_list = type_spec_kwargs[key]
                    resolved_refs[key[len("image:"):]] = [self.images[image_str] for image_str in image_list]
                else:
                    sys.stderr.write("GameObjectFactory.__create_object(): Unrecognized type '{0}'".format(
                        image_name
                    ))

            elif key.startswith("sound:"):
                sound_name = type_spec_kwargs[key]
                if isinstance(sound_name, str):
                    resolved_refs[key[len("sound:"):]] = self.sounds[sound_name]
                elif isinstance(sound_name, list):
                    sound_list = type_spec_kwargs[key]
                    resolved_refs[key[len("sound:"):]] = [self.sounds[sound_str] for sound_str in sound_list]
                else:
                    sys.stderr.write("GameObjectFactory.__create_object(): Unrecognized type '{0}'".format(
                        sound_name
                    ))

            elif key.startswith("asset:"):
                asset_name = type_spec_kwargs[key]
                if isinstance(asset_name, str):
                    resolved_refs[key[len("asset:"):]] = self.assets[asset_name]
                elif isinstance(asset_name, list):
                    inner_key = key[len("asset:"):]
                    resolved_refs[inner_key] = []
                    self.__assign_asset_list(asset_name, resolved_refs[inner_key])
                else:
                    sys.stderr.write("GameObjectFactory.__create_object(): Unrecognized type '{0}'".format(
                        asset_name
                    ))

            elif key.startswith("game_object_type:"):
                gob_type_name = type_spec_kwargs[key]
                if isinstance(gob_type_name, str):
                    resolved_refs[key[len("game_object_type:"):]] = self.create(gob_type_name, scope)
                elif isinstance(gob_type_name, list):
                    gob_type_list = type_spec_kwargs[key]
                    resolved_refs[key[len("game_object_type:"):]] = [
                        self.create(gob_type_name, scope) for gob_type_name in gob_type_list
                    ]
                else:
                    sys.stderr.write("GameObjectFactory.__create_object(): Unrecognized type '{0}'".format(
                        gob_type_name
                    ))

            elif key.startswith("type_spec:"):
                gob_type_name = type_spec_kwargs[key]
                if isinstance(gob_type_name, str):
                    resolved_refs[key[len("type_spec:"):]] = TypeSpec(self, gob_type_name)
                elif isinstance(gob_type_name, list):
                    type_list = type_spec_kwargs[key]
                    resolved_refs[key[len("type_spec:"):]] = [
                        TypeSpec(self, type_name) for type_name in type_list
                    ]
                else:
                    sys.stderr.write("GameObjectFactory.__create_object(): Unrecognized type '{0}'".format(
                        gob_type_name
                    ))
            else:
                resolved_refs[key] = type_spec_kwargs[key]

        try:
            gob_class = self.registry[type_spec["class_name"]]
            gob = gob_class(**resolved_refs, **kwargs)
            return gob
        except KeyError:
            sys.stderr.write("GameObjectBase subclass '{0}' not found.\n".format(type_spec["class_name"]))
            return None

    def __assign_asset_list(self, asset_names, asset_list):
        """
        Goes into asset_list and assigns the initialized assets to the right asset spec elements in the assets
        dictionary. This enables support for nested lists of assets in the asset specs. See the CollisionManager
        for an example of a GameObject that relies on this.
        """
        for asset_name in asset_names:
            if isinstance(asset_name, str):
                asset_list.append(self.assets[asset_name])
            else:
                asset_list.append([])
                self.__assign_asset_list(asset_name, asset_list[-1])

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
