import logging
import selectors

import message_util

from proto_reader import ProtoReader
from proto_writer import ProtoWriter


class ClientMessage:

    def __init__(self, selector, sock, addr, proto_message):
        self.selector = selector
        self.socket = sock
        self.address = addr
        self.proto_message = proto_message
        self.response = None
        self.__processed_count = 0
        self.__reader = ProtoReader(self.socket)
        self.__writer = ProtoWriter(self.socket)

    def __set_read_mode(self):
        """Sets selector to look for read events."""
        self.selector.modify(self.socket, selectors.EVENT_READ, data=self)

    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        logging.debug(f"Received response: {result}")

    def _process_response_binary_content(self):
        content = self.response
        logging.debug(f"Received response: {repr(content)}")

    def process_events(self, mask):
        """Processes events."""
        if mask & selectors.EVENT_READ:
            message = self.__reader.read()
            if message and not self.response:
                self.__process_response(**message)
                self.__reader.reset()

        if mask & selectors.EVENT_WRITE:
            self.__writer.set_buffer(self.proto_message.buffer)
            done_writing = self.__writer.write()
            logging.debug(f"Sent {self.proto_message.payload}")

            if done_writing:
                self.__set_read_mode()

    def __process_response(self, header, payload):
        if header["content-type"] == "text/json":
            encoding = header["content-encoding"]
            self.response = message_util.json_decode(payload, encoding)
            self._process_response_json_content()
        else:
            # Binary or unknown content-type
            self.response = payload
            print(
                f'received {self.jsonheader["content-type"]} response from',
                self.address,
            )
            self._process_response_binary_content()
        self.__processed_count += 1
