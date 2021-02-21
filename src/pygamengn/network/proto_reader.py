import io
import json
import struct


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
        self.__object = None

    def read(self):
        """Reads from the socket. Returns True when done reading, False otherwise."""
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
                self.__object = self.__process_message(self.__json_header, self.__buffer)
                return True

        return False

    @property
    def obj(self):
        return self.__object

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
            json_header = cls.__json_decode(buffer[:json_header_len], "utf-8")
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

    @classmethod
    def __process_message(cls, header, payload):
        """Processes the received message and returns the object contained in it."""
        obj = None
        if header["content-type"] == "text/json":
            encoding = header["content-encoding"]
            obj = cls.__json_decode(payload, encoding)
        return obj

    @classmethod
    def __json_decode(cls, json_bytes, encoding):
        """Decodes a buffer assuming it contains proper JSON. Returns the Python dictionary that represents the JSON object."""
        tiow = io.TextIOWrapper(io.BytesIO(json_bytes), encoding=encoding, newline="")
        obj = json.load(tiow)
        tiow.close()
        return obj
