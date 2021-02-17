import logging
import selectors
import struct
import sys

import message_util

from proto_reader import ProtoReader
from proto_writer import ProtoWriter


class ClientMessage:

    def __init__(self, selector, sock, addr, request):
        self.selector = selector
        self.socket = sock
        self.address = addr
        self.request = request
        self._request_queued = False
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
            if not self._request_queued:
                message = self.__queue_request()
                self.__writer.set_buffer(message)

            done_writing = self.__writer.write()
            logging.debug("Sent {0}".format(self.request["content"]))

            if done_writing:
                self.__set_read_mode()

    def close(self):
        logging.debug("Closing connection to {0}:{1}".format(self.address[0], self.address[1]))
        try:
            self.selector.unregister(self.socket)
        except Exception as e:
            logging.debug(f"selector.unregister() exception for {self.address}: {repr(e)}")

        try:
            self.socket.close()
        except OSError as e:
            logging.debug(f"socket.close() exception for {self.address}: {repr(e)}")
        finally:
            self.socket = None

    def __queue_request(self):
        content = self.request["content"]
        content_type = self.request["type"]
        content_encoding = self.request["encoding"]
        if content_type == "text/json":
            req = {
                "content_bytes": message_util.json_encode(content, content_encoding),
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        else:
            req = {
                "content_bytes": content,
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        message = message_util.create_message(**req)
        self._request_queued = True
        return message

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
