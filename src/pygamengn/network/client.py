import logging
import selectors
import socket

from client_message import ClientMessage


class Client():
    """Multiplayer client."""

    def __init__(self, address):
        self.address = address
        self.selector = selectors.DefaultSelector()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.events = selectors.EVENT_READ | selectors.EVENT_WRITE

    def connect(self):
        logging.debug("Connecting to {0}:{1}".format(self.address[0], self.address[1]))
        self.socket.connect_ex(self.address)
        request = self.create_request("search", "morpheus")
        message = ClientMessage(self.selector, self.socket, self.address, request)
        self.selector.register(self.socket, self.events, message)

    def send(self, search_string):
        request = self.create_request("search", search_string)
        message = ClientMessage(self.selector, self.socket, self.address, request)
        self.selector.modify(self.socket, self.events, message)

    def create_request(self, action, value):
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
            except ConnectionRefusedError:
                logging.debug("ConnectionRefusedError")
                message.close()

    def stop(self):
        """Stops the client."""
        logging.debug("Stop client")
        self.selector.close()


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
            client.send(search_strings[search_strings_index])
            search_strings_index = (search_strings_index + 1) % len(search_strings)

        except KeyboardInterrupt:
            client.stop()
            done = True
