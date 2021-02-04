import copy
import logging

import pygame

from game_object_base import GameObjectBase


class GameObjectFactory():
    """Factory to create GameObjectBase instances."""

    class UnknownGameType(Exception):
        """Exception raised when trying to instantiate an unknown GameObject class."""

        def __init__(self, message):
            super().__init__(message)

    def __init__(self, registry, images, sounds, assets, game_types):
        self.layer_manager = None
        self.registry = registry

        # Keys that get special treatment
        self.special_keys = [
            ("image:", lambda name: self.images[name]),
            ("sound:", lambda name: self.sounds[name]),
            ("asset:", lambda name: self.assets[name]),
            ("game_object:", lambda name: self.create(name)),
            ("type_spec:", lambda name: TypeSpec(self, name))
        ]

        # Initialize game types
        self.game_types = self.__init_game_types(game_types)

        # Load images and sounds, and initialize assets
        self.images = self.__create_assets(images, lambda v: pygame.image.load(v).convert_alpha())
        self.sounds = self.__create_assets(sounds, lambda v: pygame.mixer.Sound(v))
        self.assets = self.__create_assets(assets, lambda v: self.__create_object(v))

    def create(self, name: str, **kwargs) -> GameObjectBase:
        """Creates a GameObject instance."""
        game_type = self.__get_game_type(name)

        logging.debug("Creating {0}".format(name))

        base_type = game_type.get("base_type")
        if base_type:
            game_type = self.__build_derived_type(self.__get_game_type(base_type), game_type)

        gob = self.__create_object(game_type, **kwargs)

        # Add to groups as specified in type spec
        group_names = game_type.get("groups")
        if group_names:
            if isinstance(gob, pygame.sprite.Sprite) and self.layer_manager:
                self.layer_manager.set_layer_id(gob, name, game_type["class_name"])

            groups = [self.assets[name] for name in group_names]
            gob.add_to_groups(groups)

        # Create attachments
        attachment_specs = game_type.get("attachments")
        if gob and attachment_specs:
            for attachment_spec in attachment_specs:
                attachment_object = self.create(attachment_spec["game_type"])
                if attachment_object:
                    parent_transform = attachment_spec.get("parent_transform")
                    if parent_transform == None:
                        parent_transform = True
                    gob.attach(attachment_object, attachment_spec["offset"], parent_transform)
                    gob.transform()

        return gob

    def __build_derived_type(self, parent_type, child_type):
        """Builds a dictionary for a game type by merging the name's dictionary with its base type's."""
        merged_type = copy.deepcopy(parent_type)
        for child_key in child_type:
            if child_key != "base_type":
                self.__recursive_copy(child_type, merged_type, child_key)
        return merged_type

    def __create_object(self, type_spec, **kwargs) -> GameObjectBase:
        """Creates and returns a GameObjectBase instance from the given type specification."""
        resolved_refs = {}
        type_spec_kwargs = type_spec["kwargs"]
        for key in type_spec_kwargs:
            is_special_key = False

            for special_key in self.special_keys:
                if key.startswith(special_key[0]):
                    is_special_key = True
                    self.__resolve_refs(key, type_spec_kwargs[key], special_key, resolved_refs)

            if not is_special_key:
                resolved_refs[key] = type_spec_kwargs[key]

        try:
            gob_class = self.registry[type_spec["class_name"]]
            gob = gob_class(**resolved_refs, **kwargs)
            return gob
        except KeyError:
            logging.critical("GameObjectBase subclass '{0}' not found".format(type_spec["class_name"]))
            return None

    def __get_game_type(self, name: str) -> dict:
        """Gets the given game type, recursing into nested dictionaries as necessary."""
        keys = name.lstrip('/').split('/')
        game_type = self.game_types
        try:
            for key in keys:
                game_type = game_type[key]
            return game_type
        except KeyError:
            logging.critical("Unknown game type: {0}. Raising UnknownGameType exception".format(name))
            raise GameObjectFactory.UnknownGameType("".join(["Unknown game type: ", name]))

    def __resolve_refs(self, attribute_key, attribute_value, special_key, resolved_refs):
        """Resolves references."""
        # Get the name of the key to populate in resolved_refs
        key = attribute_key[len(special_key[0]):]

        if isinstance(attribute_value, str):
            # Simple string value -> assign it to resolved_refs
            resolved_refs[key] = special_key[1](attribute_value)

        elif isinstance(attribute_value, list):
            # The value is a list -> recurse and assign
            resolved_refs[key] = []
            self.__assign_asset_list(attribute_value, resolved_refs[key], special_key[1])
        else:
            logging.warn("Unrecognized type '{0}' for key '{1}'".format(type(attribute_value), attribute_key))

    def set_layer_manager_asset_name(self, name):
        """Sets the layer manager asset name for the factory to automatically assign layers to GameObjects."""
        layer_manager_spec = self.assets.get(name)
        if layer_manager_spec:
            self.layer_manager = layer_manager_spec
        else:
            logging.warn("LayerManager '{0}' not in inventory assets".format(name))

    def __assign_asset_list(self, asset_names, asset_list, asset_retriever):
        """
        Goes into asset_list and assigns the initialized assets to the right asset spec elements in the assets
        dictionary. This enables support for nested lists of assets in the asset specs. See the CollisionManager
        for an example of a GameObject that relies on this.
        """
        for asset_name in asset_names:
            if isinstance(asset_name, str):
                asset_list.append(asset_retriever(asset_name))
            else:
                asset_list.append([])
                self.__assign_asset_list(asset_name, asset_list[-1], asset_retriever)

    def __init_game_types(self, dictionary):
        """Mutates dictionary to ensure all references to game objects have absolute scopes."""

        def recursive_dict_iterator(dictionary, scope=[""], parent_dict=None):
            for key, value in dictionary.items():
                if type(value) is dict:
                    scope.append(key)
                    yield from recursive_dict_iterator(value, scope, value)
                    scope.pop()
                else:
                    yield (key, value, scope, parent_dict)

        for key, value, scope, parent_dict in recursive_dict_iterator(dictionary):
            if key.startswith("game_object:"):
                absolute_scope = scope[:-1]
                if type(value) is list:
                    parent_dict[key] = ["/".join(absolute_scope + [v]) if v[0] != '/' else v for v in value]
                else:
                    parent_dict[key] = "/".join(absolute_scope + [value]) if value[0] != '/' else value

        return dictionary

    def __create_assets(self, dictionary, creator_func):
        """Creates a dictionary of loaded and initialized assets using the creator_func."""
        rv = {}
        for key, value in dictionary.items():
            rv[key] = creator_func(value)
        return rv

    def __recursive_copy(self, from_obj, to_obj, key):
        """Recursively copies dictionary keys."""
        if isinstance(from_obj[key], dict):
            for subkey in from_obj[key]:
                if not key in to_obj:
                    to_obj[key] = {}
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
