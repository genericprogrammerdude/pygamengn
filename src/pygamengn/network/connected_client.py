import selectors

from server_message import ServerMessage


class ConnectedClient:
    """Server representation of a connected client."""

    def __init__(self, connection_socket, client_address, selector):
        self.socket = connection_socket
        self.address = client_address
        self.selector = selector
        self.message = None

    def activate(self):
        """Activates the connection to the client to start receiving data."""
        self.message = ServerMessage(self.selector, self.socket, self.address)
        self.selector.register(self.socket, selectors.EVENT_READ, data=self.message)
