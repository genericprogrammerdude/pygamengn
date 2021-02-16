import logging
import selectors
import socket

from connected_client import ConnectedClient


class Server():
    """
    Multiplayer server.

    This code is adapted from a Python sockets tutorial on Real Python:
    https://realpython.com/python-sockets

    Code from the tutorial:
    https://github.com/realpython/materials/tree/cdbe7ef2392ea9488badf47e405f0c7e533802f0/python-sockets-tutorial
    """

    def __init__(self, address=("localhost", 54879)):
        self.address = address
        self.selector = selectors.DefaultSelector()
        self.connected_clients = {}

    def start(self):
        """Starts the server."""
        logging.debug("Start server")
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.bind(self.address)
        self.address = lsock.getsockname()
        lsock.listen()
        logging.debug(f"Listening on {self.address[0]}:{self.address[1]}")
        lsock.setblocking(False)
        self.selector.register(lsock, selectors.EVENT_READ, data=None)

    def stop(self):
        logging.debug("Stop server")
        for address, connected_client in self.connected_clients.items():
            connected_client.close()
            logging.debug(f"Closed connection to {address[0]}:{address[1]}")
        self.selector.close()

    def tick(self):
        """Does server work."""
        events = self.selector.select(timeout=-1)
        for key, mask in events:
            if key.data is None:
                self.__accept_connection(key.fileobj)
            else:
                connected_client = key.data
                try:
                    connected_client.process_events(mask)
                except RuntimeError:
                    self.connected_clients[connected_client.address].close()
                    del self.connected_clients[connected_client.address]

    def __accept_connection(self, sock):
        """Accepts a new connection."""
        conn, addr = sock.accept()
        conn.setblocking(False)
        logging.debug(f"Accepted connection from {addr[0]}:{addr[1]}")
        connected_client = ConnectedClient(conn, addr, self.selector)
        self.connected_clients[addr] = connected_client
        connected_client.activate()


if __name__ == "__main__":
    import time
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(filename)s:%(lineno)d: %(message)s")

    server = Server()
    server.start()

    done = False
    while not done:
        try:
            server.tick()
            time.sleep(0.017)
        except KeyboardInterrupt:
            server.stop()
            done = True
