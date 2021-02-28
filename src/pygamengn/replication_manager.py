import logging

from game_object_base import GameObjectBase
from class_registrar import ClassRegistrar
from network.client import Client
from network.server import Server


@ClassRegistrar.register("ReplicationManager")
class ReplicationManager(GameObjectBase):
    """
    Manages GameObjects that are marked for replication.
    """

    def __init__(self):
        super().__init__()
        self.__replicators = {}
        self.__client = None
        self.__server = None

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

    def __get_replication_data(self):
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

    def __apply_replication_data(self):
        """
        Applies the data received by the client to the registered game objects.

        The client calls this function at the end of each game update to ensure that all the replicated game objects
        are in sync with their primary replicas existing on the server.
        """
        pass

    def start_replication(self):
        """Starts replication."""
        # HACK ALERT! #
        if self.__find_local_server():
            # Found a local server running -> connect to it
            self.__client = Client(("localhost", 54879))
            self.__client.connect("Player2")
        else:
            # No local server running -> run one
            self.__server = Server()
            self.__server.start()
        # HACK ALERT! #

    def update(self, delta):
        if self.__client:
            self.__client.tick()

    @classmethod
    def __find_local_server(cls):
        """Tries to connect to a local server. Returns True if successful, False otherwise."""
        client = Client(("localhost", 54879))
        client.connect("Player2")

        found_server = False
        try:
            client.tick()
            found_server = True
        except BrokenPipeError:
            pass
        finally:
            client.stop()

        return found_server
