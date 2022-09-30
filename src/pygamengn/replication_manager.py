import logging

from pygamengn.game_object_base import GameObjectBase
from pygamengn.class_registrar import ClassRegistrar
from pygamengn.network.client import Client
from pygamengn.network.client import ClientState
from pygamengn.network.server import Server


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

    def __compile_replication_data(self):
        """
        Compiles and returns the dictionary with the data for all the register replicators.

        The server calls this function after all the game objects have been updated. The compiled data is sent by
        the server to all the connected clients.
        """
        replication_data = {}
        for rep_id, gob in self.__replicators.items():
            replication_data[rep_id] = {}
            for rep_prop in gob.get_replicated_props():
                replication_data[rep_id][rep_prop.name] = rep_prop.packer.pack(getattr(gob, rep_prop.getter))
        return replication_data

    def __apply_replication_data(self, game_state):
        """
        Applies the data received by the client to the registered game objects.

        The client calls this function at the end of each game update to ensure that all the replicated game objects
        are in sync with their primary replicas existing on the server.
        """
        for replication_id, replication_data in game_state.items():
            gob = self.__replicators.get(replication_id)
            if gob:
                for rep_prop in gob.get_replicated_props():
                    new_value = replication_data.get(rep_prop.name)
                    if new_value:
                        setattr(gob, rep_prop.setter, rep_prop.packer.unpack(new_value))

    def start_replication(self):
        """Starts replication."""
        # HACK ALERT! #
        if self.__find_local_server():
            # Found a local server running -> connect to it
            self.__client = Client(("localhost", 54879))
            self.__client.connect("Player2")
            logging.debug("Started client")
        else:
            # No local server running -> run one
            self.__server = Server()
            self.__server.start()
            logging.debug("Started server")
        # HACK ALERT! #

    def update(self, delta):
        """Updates the replication manager."""
        if self.__client:
            if self.__client.tick():
                if self.__client.state == ClientState.PLAYING:
                    self.__apply_replication_data(self.__client.get_game_state())
                    self.__client.reset_game_state()
            else:
                self.__client = None

        elif self.__server:
            self.__server.propagate_game_state(self.__compile_replication_data())
            self.__server.tick()

    def propagate_input(self, inputs):
        """Sets the list of input actions collected by the game in the current frame. These are sent to the server."""
        if self.__client:
            self.__client.set_inputs(inputs)

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
