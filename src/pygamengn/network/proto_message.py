import json
import struct
import sys


class ProtoMessage:
    """Protocol message that can be sent between pygamengn Client and Server."""

    def __init__(self, payload):
        self.__payload = payload
        self.__buffer = None

    def build(self):
        """Builds the protocol message and leaves the buffer ready for sending."""
        content_type = "text/json"
        content_encoding = "utf-8"
        content_bytes = self.__json_encode(self.__payload, content_encoding)

        json_header = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        json_header_bytes = self.__json_encode(json_header, "utf-8")
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
    def __json_encode(cls, content, content_encoding):
        """Encodes the given content as a JSON object."""
        return json.dumps(content, ensure_ascii=False).encode(content_encoding)

    ###################
    # Client messages
    ###################

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
    def ready_message(cls):
        """Builds and returns a READY message to send from the Client to the Server."""
        message = ProtoMessage({
            "message": "READY"
        })
        message.build()
        return message

    @classmethod
    def input_message(cls, inputs):
        """Builds and returns a READY message to send from the Client to the Server."""
        message = ProtoMessage({
            "message": "INPUT",
            "inputs": inputs
        })
        message.build()
        return message

    ###################
    # Server messages
    ###################

    @classmethod
    def init_message(cls, objects_dict):
        """Builds and returns an INIT message to send from the Server to the Client."""
        message = ProtoMessage({
            "message": "INIT",
            "objects": objects_dict
        })
        message.build()
        return message

    @classmethod
    def start_message(cls):
        """Builds and returns a START message to send from the Server to the Client."""
        message = ProtoMessage({
            "message": "START"
        })
        message.build()
        return message

    @classmethod
    def update_message(cls, objects_dict):
        """Builds and returns an UPDATE message to send from the Server to the Client."""
        message = ProtoMessage({
            "message": "UPDATE",
            "objects": objects_dict
        })
        message.build()
        return message

    @classmethod
    def stop_message(cls):
        """Builds and returns a STOP message to send from the Server to the Client."""
        message = ProtoMessage({
            "message": "STOP"
        })
        message.build()
        return message
