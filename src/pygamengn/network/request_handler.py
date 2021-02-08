import logging
import socketserver


class RequestHandler(socketserver.BaseRequestHandler):
    """Handler for requests received by the server."""

    def handle(self):
        logging.debug("handle()")
        data = self.request.recv(2048)
        logging.debug(data)
        self.request.send(data)

    def finish(self):
        logging.debug("finish()")
        return super().finish()

    def receive(self):
        chunks = []
        chunk = self.request.recv(2048)
        while len(chunk) > 0:
            chunks.append(chunk)
            chunk = self.request.recv(2048)
        return b"".join(chunks)
