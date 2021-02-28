import logging

from game_object_base import GameObjectBase
from class_registrar import ClassRegistrar


@ClassRegistrar.register("ReplicationManager")
class ReplicationManager(GameObjectBase):
    """
    Manages GameObjects that are marked for replication.
    """

    def __init__(self):
        super().__init__()
        self.__replicators = {}

    def add_object(self, replication_id, gob):
        """Adds a GameObject to be replicated from server to connected clients."""
        self.__replicators[replication_id] = gob

        # DEBUG #
        logging.debug(f"Added {gob}")
        logging.debug(self.__replicators)
        for rep_id, gob in self.__replicators.items():
            logging.debug(rep_id)
            for prop in gob.get_replicated_props():
                logging.debug(prop)
        # DEBUG #

    def get_replication_data(self):
        """
        Compiles and returns the dictionary with the data for all the register replicators.

        The server calls this function after all the game objects have been updated. The compiled data is sent by
        the server to all the connected clients.
        """
        replication_data = {}
        for rep_id, gob in self.__replicators.items():
            replication_data[rep_id] = {}
            for prop in gob.get_replicated_props():
                replication_data[rep_id][prop] = getattr(gob, prop)
        return replication_data

    def apply_replication_data(self):
        """
        Applies the data received by the client to the registered game objects.

        The client calls this function at the end of each game update to ensure that all the replicated game objects
        are in sync with their primary replicas existing on the server.
        """
        pass
