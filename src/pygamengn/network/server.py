import logging
import selectors
import socket

from pygamengn.network.connected_client import ConnectedClient
from pygamengn.network.proto_message import ProtoMessage


class Server():
    """Multiplayer server."""

    def __init__(self, address=("localhost", 54879)):
        self.__address = address
        self.__selector = selectors.DefaultSelector()
        self.__connected_clients = {}

    def start(self):
        """Starts the server."""
        logging.debug("Start server")
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.bind(self.__address)
        self.__address = lsock.getsockname()
        lsock.listen()
        logging.debug(f"Listening on {self.__address[0]}:{self.__address[1]}")
        lsock.setblocking(False)
        self.__selector.register(lsock, selectors.EVENT_READ)

    def stop(self):
        logging.debug("Stop server")
        for address, connected_client in self.__connected_clients.items():
            connected_client.close()
            logging.debug(f"Closed connection to {address[0]}:{address[1]}")
        self.__selector.close()

    def tick(self):
        """Does server work."""
        events = self.__selector.select(timeout=-1)
        for key, mask in events:
            if key.data is None:
                self.__accept_connection(key.fileobj)
            else:
                connected_client = key.data
                try:
                    connected_client.process_events(mask)
                except (RuntimeError, ConnectionResetError) as e:
                    logging.debug(f"Client disconnected: {e}")
                    self.__connected_clients[connected_client.address].close()
                    del self.__connected_clients[connected_client.address]

    def propagate_game_state(self, game_state_dict):
        """Propagates the dictionary that represents game state to all the connected clients."""
        message = ProtoMessage.update_message(game_state_dict)
        for _, client in self.__connected_clients.items():
            client.set_game_state_message(message)

    def __accept_connection(self, sock):
        """Accepts a new connection."""
        conn, addr = sock.accept()
        conn.setblocking(False)
        logging.debug(f"Accepted connection from {addr[0]}:{addr[1]}")
        connected_client = ConnectedClient(conn, addr, self.__selector, [640, 360])
        self.__connected_clients[addr] = connected_client
        connected_client.activate()
