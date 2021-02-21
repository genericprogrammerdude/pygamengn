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
        content_type = "text/json"
        content_encoding = "utf-8"
        content_bytes = message_util.json_encode(self.__payload, content_encoding)

        json_header = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        json_header_bytes = message_util.json_encode(json_header, "utf-8")
        message_hdr = struct.pack(">H", len(json_header_bytes))
        self.__buffer = message_hdr + json_header_bytes + content_bytes

    def reset(self):
        self.__payload = None
        self.__buffer = None

    @property
    def buffer(self):
        return self.__buffer

    @property
    def payload(self):
        return self.__payload

    @classmethod
    def connect_message(cls, player_name):
        """Builds and returns a CONNECT message to send from the Client to the Server."""
        message = ProtoMessage({
            "message": "CONNECT",
            "name": player_name
        })
        message.build()
        return message

    @classmethod
    def init_message(cls, objects_dict):
        """Builds and returns a CONNECT message to send from the Client to the Server."""
        message = ProtoMessage({
            "message": "INIT",
            "objects": objects_dict
        })
        message.build()
        return message
