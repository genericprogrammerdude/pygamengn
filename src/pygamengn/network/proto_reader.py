import struct

import message_util


class ProtoReader:
    """ProtoReader worker for the pygamengn protocol."""

    def __init__(self, sock):
        self.__sock = sock
        self.reset()

    def reset(self):
        """Resets the reader so it can start reading a new message."""
        self.__buffer = b""
        self.__json_header_len = None
        self.__json_header = None

    def read(self):
        self.__read()

        if not self.__json_header_len:
            self.__json_header_len, self.__buffer = self.__process_protoheader(self.__buffer)

        if self.__json_header_len and not self.__json_header:
            self.__json_header, self.__buffer = self.__process_json_header(
                self.__json_header_len,
                self.__buffer
            )

            content_len = self.__json_header["content-length"]
            if len(self.__buffer) == content_len:
                return {
                    "header": self.__json_header,
                    "payload": self.__buffer
                }

        return None

    def __read(self):
        try:
            # Should be ready to read
            data = self.__sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self.__buffer += data
            else:
                raise RuntimeError("Peer closed.")

    @classmethod
    def __process_protoheader(cls, buffer):
        """Reads the protocol header length and returns the message length and message (without the header length bytes)."""
        header_len = 2
        if len(buffer) >= header_len:
            json_header_len = struct.unpack(">H", buffer[:header_len])[0]
            buffer = buffer[header_len:]
            return (json_header_len, buffer)
        else:
            return (None, buffer)

    @classmethod
    def __process_json_header(cls, json_header_len, buffer):
        """Reads the JSON header contained in the buffer, assuming the the buffer is json_header_len bytes long."""
        if len(buffer) >= json_header_len:
            json_header = message_util.json_decode(buffer[:json_header_len], "utf-8")
            buffer = buffer[json_header_len:]
            cls.__validate_json_header(json_header)
            return (json_header, buffer)
        else:
            return (None, buffer)

    @classmethod
    def __validate_json_header(cls, json_header):
        for required_field in ("byteorder", "content-length", "content-type", "content-encoding"):
            if required_field not in json_header:
                raise ValueError(f'Missing required header "{required_field}".')
