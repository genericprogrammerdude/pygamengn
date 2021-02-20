import struct
import sys

import message_util


class ProtoMessage:
    """Protocol message that can be sent between pygamengn Client and Server."""

    def __init__(self, payload):
        self.__payload = payload
        self.__buffer = None

    def build(self):
        """Builds the protocol message and leaves the buffer ready for sending."""
        content = dict(action="search", value=self.__payload)
        content_type = "text/json"
        content_encoding = "utf-8"
        content_bytes = message_util.json_encode(content, content_encoding)

        json_header = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        json_header_bytes = message_util.json_encode(json_header, "utf-8")
        message_hdr = struct.pack(">H", len(json_header_bytes))
        self.__buffer = message_hdr + json_header_bytes + content_bytes

    @property
    def buffer(self):
        return self.__buffer

    @property
    def payload(self):
        return self.__payload
