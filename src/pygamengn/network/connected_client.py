import logging
import selectors

from proto_message import ProtoMessage
from proto_reader import ProtoReader
from proto_writer import ProtoWriter


class ConnectedClient:
    """Server representation of a connected client."""

    def __init__(self, connection_socket, client_address, selector):
        self.socket = connection_socket
        self.address = client_address
        self.selector = selector
        self.__reader = ProtoReader(self.socket)
        self.__writer = ProtoWriter(self.socket)
        self.__reset()
        self.__processed_count = 0

    def __reset(self):
        self.request = None
        self.response_created = False
        self.__reader.reset()

    def activate(self):
        """Activates the connection to the client to start receiving data."""
        self.selector.register(self.socket, selectors.EVENT_READ, data=self)

    def __set_read_mode(self):
        """Sets selector to look for read events."""
        self.selector.modify(self.socket, selectors.EVENT_READ, data=self)

    def __set_write_mode(self):
        """Sets selector to look for write events."""
        self.selector.modify(self.socket, selectors.EVENT_WRITE, data=self)

    def process_events(self, mask):
        """Processes events."""
        if mask & selectors.EVENT_READ:
            done_reading = self.__reader.read()
            if done_reading and not self.request:
                self.__process_request(self.__reader.obj)
                self.__reader.reset()

        if mask & selectors.EVENT_WRITE:
            if self.request:
                if not self.response_created:
                    message = self.__create_response()
                    self.__writer.set_buffer(message.buffer)
                if self.__writer.write():
                    logging.debug(f"Sent response to {self.address[0]}:{self.address[1]}")
                    self.__reset()
                    self.__set_read_mode()

    def close(self):
        """Closes the connection to the client."""
        logging.debug(f"Closing connection to {self.address[0]}:{self.address[1]}")
        try:
            self.selector.unregister(self.socket)
        except Exception as e:
            logging.error(f"selector.unregister() exception for {self.address}: {repr(e)}")

        try:
            self.socket.close()
        except OSError as e:
            logging.error(f"socket.close() exception for {self.address}: {repr(e)}")
        finally:
            self.socket = None

    def __process_request(self, dict):
        self.request = dict
        logging.debug(f"Received request {repr(self.request)} from {self.address[0]}:{self.address[1]}")
        # Set selector to listen for write events, we're done reading.
        self.__set_write_mode()
        self.__processed_count += 1

    def __create_response(self):
        message = self.request.get("message")

        if message == "CONNECT":
            self.__player_name = self.request["name"]
            print(self.__player_name)

            message = ProtoMessage.init_message({})
            self.response_created = True
            return message
