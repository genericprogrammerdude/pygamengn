import logging

from pygamengn.class_registrar import ClassRegistrar
from pygamengn.game_object_base import GameObjectBase


@ClassRegistrar.register("LayerManager")
class LayerManager(GameObjectBase):
    """
    Manages draw layers semi-automatically.

    The order of GameObject subclasses defined in self.layers determines the draw order. Abstract game types
    declared in the inventory file can also be used in self.layers.

    GameObjectFactory sets the 'layer' constructor argument in every GameObject instance it creates. The value of
    the parameter comes from the object's class or abstract game type, as defined in LayerManager's 'layers' list.
    """

    INVALID_LAYER_ID = -1

    def __init__(self, layers):
        self.layers = layers

    def get_layer_id(self, name):
        """Returns the layer for the given game type name."""
        for index, layer in enumerate(self.layers):
            if name in layer:
                return index
        return self.INVALID_LAYER_ID

    def set_layer_id(self, gob, scoped_name, class_name):
        """Sets the gob's layer id using scoped_name first and class_name second to find the right layer."""
        # Get layer id for the GameObject only if it's in the RenderGroup
        layer_id = self.get_layer_id(scoped_name)
        if layer_id == self.INVALID_LAYER_ID:
            layer_id = self.get_layer_id(class_name)

        if layer_id != LayerManager.INVALID_LAYER_ID:
            gob.set_layer_id(layer_id)
        else:
            logging.warn(
                "Game type name '{0}' of class '{1}' doesn't have an assigned layer in LayerManager".format(
                    scoped_name,
                    class_name
                )
            )
