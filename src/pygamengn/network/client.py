import logging
import selectors
import socket

from client_message import ClientMessage
from proto_message import ProtoMessage


class Client():
    """Multiplayer client."""

    def __init__(self, address):
        self.address = address
        self.selector = selectors.DefaultSelector()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.events = selectors.EVENT_READ | selectors.EVENT_WRITE

    def connect(self):
        """Connects to the server."""
        logging.debug("Connecting to {0}:{1}".format(self.address[0], self.address[1]))
        self.socket.connect_ex(self.address)
        request = self.__create_request("search", "morpheus")
        message = ClientMessage(self.selector, self.socket, self.address, request)
        self.selector.register(self.socket, self.events, message)

    def send(self, search_string):
        """Sends a message to the server. Assumes that selector and socket are valid and in good state."""
        request = self.__create_request("search", search_string)
        proto_message = ProtoMessage(search_string)
        proto_message.build()
        message = ClientMessage(self.selector, self.socket, self.address, proto_message)
        self.selector.modify(self.socket, self.events, message)

    def tick(self):
        """Does client work."""
        if not self.selector.get_map():
            logging.error("Client ticking but not connected to server")
            return

        events = self.selector.select(timeout=-1)
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
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

    def __create_request(self, action, value):
        if action == "search":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action, value=value),
            )
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(action + value, encoding="utf-8"),
            )


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
            time.sleep(0.5)
            try:
                client.send(search_strings[search_strings_index])
                search_strings_index = (search_strings_index + 1) % len(search_strings)
            except ValueError:
                logging.debug("Client socket is invalid")
                done = True

        except KeyboardInterrupt:
            client.stop()
            done = True
