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
            self.__json_header_len, self.__buffer = message_util.process_protoheader(self.__buffer)

        if self.__json_header_len and not self.__json_header:
            self.__json_header, self.__buffer = message_util.process_json_header(
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
