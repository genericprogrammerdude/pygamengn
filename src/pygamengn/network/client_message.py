import io
import json
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
        self._send_buffer = b""
        self._request_queued = False
        self.response = None
        self.__processed_count = 0
        self.__reader = ProtoReader(self.socket)
        self.__writer = ProtoWriter(self.socket)

    def __set_read_mode(self):
        """Sets selector to look for read events."""
        self.selector.modify(self.socket, selectors.EVENT_READ, data=self)

    def _write(self):
        if self._send_buffer:
            # logging.debug("Sending {0} to {1}:{2}".format(repr(self._send_buffer), self.address[0], self.address[1]))
            try:
                # Should be ready to write
                sent = self.socket.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]

    def _create_message(self, content_bytes, content_type, content_encoding):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = message_util.json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        logging.debug(f"Received response: {result}")

    def _process_response_binary_content(self):
        content = self.response
        logging.debug(f"Received response: {repr(content)}")

    def FROM_CONNECTED_CLIENT_process_events(self, mask):
        """Processes events."""
        if mask & selectors.EVENT_READ:
            message = self.__reader.read()
            if message and not self.request:
                self.__process_request(**message)

        if mask & selectors.EVENT_WRITE:
            if self.request:
                if not self.response_created:
                    message = self.__create_response()
                    self.__writer.set_buffer(message)
                if self.__writer.write():
                    logging.debug(f"Sent response to {self.address[0]}:{self.address[1]}")
                    self.__reset()
                    self.__set_read_mode()

    def process_events(self, mask):
        """Processes events."""
        if mask & selectors.EVENT_READ:
            message = self.__reader.read()
            if message and not self.response:
                self.__process_response(**message)

        if mask & selectors.EVENT_WRITE:
            self.write()

    def write(self):
        if not self._request_queued:
            self.queue_request()

        self._write()
        logging.debug("Sent {0}".format(self.request["content"]))

        if self._request_queued:
            if not self._send_buffer:
                self.__set_read_mode()

    def close(self):
        logging.debug("Closing connection to {0}:{1}".format(self.address[0], self.address[1]))
        try:
            self.selector.unregister(self.socket)
        except Exception as e:
            print(
                "error: selector.unregister() exception for",
                f"{self.address}: {repr(e)}",
            )

        try:
            self.socket.close()
        except OSError as e:
            print(
                "error: socket.close() exception for",
                f"{self.address}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.socket = None

    def queue_request(self):
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
        message = self._create_message(**req)
        self._send_buffer += message
        self._request_queued = True

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
        # Close when response has been processed
        self.__processed_count += 1
