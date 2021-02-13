import logging
import socketserver
import threading

from network.request_handler import RequestHandler


class Server():
    """Create a server to listen to clients and broadcast data."""

    def __init__(self):
        self.address = ("localhost", 0)
        self.client_name = " "
        self.clients = []
        self.client_names = []

    def start(self):
        """Starts the server."""
        logging.debug("Server.start()")

        self.server = socketserver.ThreadingTCPServer(self.address, RequestHandler)
        self.address = self.server.server_address
        logging.debug("server address: {0}:{1}".format(self.address[0], self.address[1]))

        self.server_thread = threading.Thread(target=self.server.serve_forever, name="pygamengn-server")
        self.server_thread.daemon = True
        self.server_thread.start()
        logging.debug("Server loop running in {0}".format(self.server_thread.getName()))

    def stop(self):
        logging.debug("Server.stop()")
        self.server_thread.join(0.5)
        self.server.shutdown()
        self.server.server_close()
