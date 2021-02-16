import message_util


class ProtoWriter:
    """ProtoWriter worker for the pygamengn protocol."""

    def __init__(self, sock):
        self.__sock = sock
        self.reset()

    def reset(self):
        """Resets the reader so it can start reading a new message."""
        self.__buffer = b""

    def set_buffer(self, buffer):
        """Sets the buffer to write to the socket."""
        self.__buffer = buffer

    def write(self):
        """Writes to the socket and returns True when the entire buffer has been sent."""
        if self.__buffer:
            try:
                # Should be ready to write
                sent = self.__sock.send(self.__buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self.__buffer = self.__buffer[sent:]
                if sent and not self.__buffer:
                    return True
        return False
