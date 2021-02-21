import logging
import selectors
import socket

from proto_message import ProtoMessage
from proto_reader import ProtoReader
from proto_writer import ProtoWriter


class Client():
    """Multiplayer client."""

    def __init__(self, address):
        self.address = address
        self.selector = selectors.DefaultSelector()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.__proto_message = None
        self.__processed_count = 0
        self.__reader = ProtoReader(self.socket)
        self.__writer = ProtoWriter(self.socket)

    def connect(self):
        """Connects to the server."""
        logging.debug("Connecting to {0}:{1}".format(self.address[0], self.address[1]))
        self.socket.connect_ex(self.address)
        self.__proto_message = ProtoMessage.connect_message("Player2")
        self.__proto_message.build()
        self.selector.register(self.socket, selectors.EVENT_WRITE)

    def tick(self):
        """Does client work."""
        if not self.selector.get_map():
            logging.error("Client ticking but not connected to server")
            return

        events = self.selector.select(timeout=-1)
        for _, mask in events:
            try:
                self.__process_events(mask)
            except (RuntimeError, ConnectionRefusedError, ConnectionResetError) as e:
                logging.debug(f"Client disconnected: {e}")
                self.stop()

    def stop(self):
        """Stops the client."""
        logging.debug("Stop client")
        try:
            self.selector.unregister(self.socket)
        except Exception as e:
            logging.debug(f"selector.unregister() exception for {self.address}: {repr(e)}")

        try:
            self.socket.close()
        except OSError as e:
            logging.debug(f"socket.close() exception for {self.address}: {repr(e)}")
        finally:
            self.socket = None
        self.selector.close()

    def __process_events(self, mask):
        """Processes events."""
        if mask & selectors.EVENT_READ:
            done_reading = self.__reader.read()
            if done_reading:
                self.__process_response(self.__reader.obj)
                self.__reader.reset()
                self.__set_write_mode()

        if mask & selectors.EVENT_WRITE:
            assert self.__proto_message.buffer
            self.__writer.set_buffer(self.__proto_message.buffer)
            done_writing = self.__writer.write()
            logging.debug(f"Sent {self.__proto_message.payload}")

            if done_writing:
                self.__proto_message.reset()
                self.__set_read_mode()

    def __process_response(self, dictionary):
        logging.debug(f"Received response: {dictionary}")
        self.__processed_count += 1

    def __set_read_mode(self):
        """Sets selector to look for read events."""
        self.selector.modify(self.socket, selectors.EVENT_READ)

    def __set_write_mode(self):
        """Sets selector to look for write events."""
        self.selector.modify(self.socket, selectors.EVENT_WRITE)


if __name__ == "__main__":
    import time
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(filename)s:%(lineno)d: %(message)s")

    search_strings = ["morpheus", "ring", "\U0001f436"]
    search_strings_index = 1

    client = Client(("localhost", 54879))
    client.connect()

    done = False
    while not done:
        try:
            client.tick()
            time.sleep(0.02)

        except (AssertionError, KeyboardInterrupt):
            client.stop()
            done = True
