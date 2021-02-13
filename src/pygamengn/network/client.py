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
        try:
            data = self.sock.recv(2048).decode()
        except ConnectionResetError:
            logging.debug("ConnectionResetError. Re-connecting")
            self.connect()
            data = None
        if data:
            logging.debug("Received {0} bytes".format(len(data)))
        return data
