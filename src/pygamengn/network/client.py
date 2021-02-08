import logging
import socket


class Client():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

    def send(self, message):
        sent_count = 0
        self.message = message
        while sent_count < len(message):
            sent = self.sock.send(message[sent_count:])
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            sent_count += sent
        logging.debug("Sent {0} bytes".format(sent_count))

    def receive(self):
        chunks = []
        received_count = 0
        while received_count < len(self.message):
            chunk = self.sock.recv(min(len(self.message) - received_count, 2048))
            if chunk == b"":
                logging.debug("Socket connection broken")
            else:
                chunks.append(chunk)
                received_count += len(chunk)
                logging.debug("Received {0}/{1} bytes".format(received_count, len(self.message)))
        return b"".join(chunks)
