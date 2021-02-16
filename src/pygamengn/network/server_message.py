import logging
import selectors

import message_util

from proto_reader import ProtoReader
from proto_writer import ProtoWriter


class ServerMessage:

    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.reader = ProtoReader(sock)
        self.writer = ProtoWriter(sock)
        self.__reset()
        self.__processed_count = 0

    def __reset(self):
        self.request = None
        self.response_created = False
        self.reader.reset()
        self.writer.reset()

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            message = self.reader.read()
            if message and not self.request:
                self.process_request(**message)

        if mask & selectors.EVENT_WRITE:
            if self.request:
                if not self.response_created:
                    message = self.create_response()
                    self.writer.set_buffer(message)
                if self.writer.write():
                    self.__reset()
                    self._set_selector_events_mask("r")

    def close(self):
        logging.debug("Closing connection to {0}:{1}".format(self.addr[0], self.addr[1]))
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            logging.error(f"selector.unregister() exception for {self.addr}: {repr(e)}")

        try:
            self.sock.close()
        except OSError as e:
            logging.error(f"socket.close() exception for {self.addr}: {repr(e)}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def process_request(self, header, payload):
        if header["content-type"] == "text/json":
            encoding = header["content-encoding"]
            self.request = message_util.json_decode(payload, encoding)
            logging.debug("Received request {0} from {1}:{2}".format(repr(self.request), self.addr[0], self.addr[1]))
        else:
            # Binary or unknown content-type
            self.request = payload
            logging.debug(f"Received {header['content-type']} request from {self.addr}")

        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")
        self.__processed_count += 1

    def create_response(self):
        action = self.request.get("action")
        value = self.request.get("value")
        response = message_util.create_response_json_content(action, value)
        message = message_util.create_message(**response)
        self.response_created = True
        return message
