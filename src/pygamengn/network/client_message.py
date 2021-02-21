import logging
import selectors

from proto_reader import ProtoReader
from proto_writer import ProtoWriter


class ClientMessage:

    def __init__(self, selector, sock, addr, proto_message):
        self.selector = selector
        self.socket = sock
        self.address = addr
        self.__proto_message = proto_message
        self.response = None
        self.__processed_count = 0
        self.__reader = ProtoReader(self.socket)
        self.__writer = ProtoWriter(self.socket)

    def __set_read_mode(self):
        """Sets selector to look for read events."""
        self.selector.modify(self.socket, selectors.EVENT_READ, data=self)

    def process_events(self, mask):
        """Processes events."""
        if mask & selectors.EVENT_READ:
            done_reading = self.__reader.read()
            if done_reading:
                self.__process_response(self.__reader.obj)
                self.__reader.reset()

        if mask & selectors.EVENT_WRITE:
            self.__writer.set_buffer(self.__proto_message.buffer)
            done_writing = self.__writer.write()
            logging.debug(f"Sent {self.__proto_message.payload}")

            if done_writing:
                self.__proto_message.reset()
                self.__set_read_mode()

    def __process_response(self, dict):
        logging.debug(f"Received response: {dict}")
        self.__processed_count += 1
