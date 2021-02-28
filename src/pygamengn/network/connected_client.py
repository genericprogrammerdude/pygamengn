import logging
import selectors

from network.proto_message import ProtoMessage
from network.proto_reader import ProtoReader
from network.proto_writer import ProtoWriter


class ConnectedClient:
    """Server representation of a connected client."""

    def __init__(self, connection_socket, client_address, selector):
        self.__socket = connection_socket
        self.address = client_address
        self.__selector = selector
        self.__reader = ProtoReader(self.__socket)
        self.__writer = ProtoWriter(self.__socket)
        self.__reset()
        self.__processed_count = 0
        self.__game_state_message = {}

    def __reset(self):
        self.request = None
        self.response_created = False
        self.__reader.reset()

    def activate(self):
        """Activates the connection to the client to start receiving data."""
        self.__selector.register(self.__socket, selectors.EVENT_READ, data=self)

    def set_game_state_message(self, game_state_message: ProtoMessage):
        """Sets the ProtoMessage that represents game state to be propagated to the client."""
        self.__game_state_message = game_state_message

    def __set_read_mode(self):
        """Sets selector to look for read events."""
        self.__selector.modify(self.__socket, selectors.EVENT_READ, data=self)

    def __set_write_mode(self):
        """Sets selector to look for write events."""
        self.__selector.modify(self.__socket, selectors.EVENT_WRITE, data=self)

    def process_events(self, mask):
        """Processes events."""
        if mask & selectors.EVENT_READ:
            done_reading = self.__reader.read()
            if done_reading and not self.request:
                if not self.__process_request(self.__reader.obj):
                    # The client sent a DROP request -> shut the connection down
                    self.close()
                self.__reader.reset()

        if mask & selectors.EVENT_WRITE:
            if self.request:
                if not self.response_created:
                    message = self.__create_response()
                    logging.debug(f"Sending {message.payload} to {self.address[0]}:{self.address[1]}")
                    self.__writer.set_buffer(message.buffer)
                if self.__writer.write():
                    logging.debug(f"Sent response to {self.address[0]}:{self.address[1]}")
                    self.__reset()
                    self.__set_read_mode()

    def close(self):
        """Closes the connection to the client."""
        logging.debug(f"Closing connection to {self.address[0]}:{self.address[1]}")
        try:
            self.__selector.unregister(self.__socket)
        except Exception as e:
            logging.error(f"selector.unregister() exception for {self.address}: {repr(e)}")

        try:
            self.__socket.close()
        except OSError as e:
            logging.error(f"socket.close() exception for {self.address}: {repr(e)}")
        finally:
            self.__socket = None

    def __process_request(self, dictionary):
        self.request = dictionary
        self.__processed_count += 1
        logging.debug(f"Received request {repr(self.request)} from {self.address[0]}:{self.address[1]}")
        if dictionary["message"] == "DROP":
            return False
        self.__set_write_mode()
        return True

    def __create_response(self):
        message = self.request.get("message")

        if message == "CONNECT":
            self.__player_name = self.request["name"]
            response = ProtoMessage.init_message({
                "object1": {
                    "game_type": "/Some/gob_type/from/inventory",
                    "pos": [23, 32],
                    "heading": 54,
                    "health": 100
                },
                "Player1": {
                    "game_type": "/Ship",
                    "pos": (0, 2),
                    "heading": 0,
                    "health": 58
                }
            })
            self.response_created = True
            return response

        elif message == "READY":
            response = ProtoMessage.start_message()
            self.response_created = True
            return response

        elif message == "INPUT":
            response = self.__game_state_message
            self.response_created = True
            return response

        return None
