import logging
import selectors
import socket

from client_message import ClientMessage


class Client():
    """
    Multiplayer client.

    This code is adapted from a Python sockets tutorial on Real Python:
    https://realpython.com/python-sockets

    Code from the tutorial:
    https://github.com/realpython/materials/tree/cdbe7ef2392ea9488badf47e405f0c7e533802f0/python-sockets-tutorial
    """

    def __init__(self, address):
        self.address = address
        self.selector = selectors.DefaultSelector()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.events = selectors.EVENT_READ | selectors.EVENT_WRITE

    def connect(self):
        logging.debug("Connecting to {0}:{1}".format(self.address[0], self.address[1]))
        self.sock.connect_ex(self.address)
        request = self.create_request("search", "morpheus")
        message = ClientMessage(self.selector, self.sock, self.address, request)
        self.selector.register(self.sock, self.events, message)

    def send(self, search_string):
        request = self.create_request("search", search_string)
        message = ClientMessage(self.selector, self.sock, self.address, request)
        self.selector.modify(self.sock, self.events, message)

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
            except Exception:
                print(
                    "main: error: exception for",
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
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
