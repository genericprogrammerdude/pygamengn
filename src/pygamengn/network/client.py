from enum import Enum, auto

import logging
import selectors
import socket

from proto_message import ProtoMessage
from proto_reader import ProtoReader
from proto_writer import ProtoWriter
from fsm import FiniteStateMachine, FSMTransition


class ClientState(Enum):
    DISCONNECTED = auto()
    CONNECTED = auto()
    READY = auto()
    PLAYING = auto()


class ClientInput(Enum):
    INIT = "INIT"
    START = "START"
    UPDATE = "UPDATE"
    STOP = "STOP"


class Client():
    """Multiplayer client."""

    def __init__(self, address):
        self.__address = address
        self.__selector = selectors.DefaultSelector()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setblocking(False)
        self.__proto_message = None
        self.__processed_count = 0
        self.__reader = ProtoReader(self.__socket)
        self.__writer = ProtoWriter(self.__socket)
        self.__fsm = FiniteStateMachine(ClientState.DISCONNECTED, {
            ClientState.DISCONNECTED: {
                ClientInput.INIT: FSMTransition(ClientState.CONNECTED, self.command_init)
            },
            ClientState.CONNECTED: {
                ClientInput.START: FSMTransition(ClientState.PLAYING)
            },
            ClientState.PLAYING: {
                ClientInput.UPDATE: FSMTransition(ClientState.PLAYING, self.command_update),
                ClientInput.STOP: FSMTransition(ClientState.DISCONNECTED, self.command_stop)
            }
        })

    def connect(self, player_name):
        """Connects to the server."""
        logging.debug("Connecting to {0}:{1}".format(self.__address[0], self.__address[1]))
        self.__socket.connect_ex(self.__address)
        self.__proto_message = ProtoMessage.connect_message(player_name)
        self.__selector.register(self.__socket, selectors.EVENT_WRITE)

    def tick(self):
        """Does client work."""
        if not self.__selector.get_map():
            logging.error("Client ticking but not connected to server")
            return

        events = self.__selector.select(timeout=-1)
        for _, mask in events:
            try:
                self.__process_events(mask)
            except (RuntimeError, ConnectionRefusedError, ConnectionResetError) as e:
                logging.debug(f"Client disconnected: {e}")
                self.stop()

    def stop(self):
        """Stops the client."""
        logging.debug("Stop client")
        try:
            self.__selector.unregister(self.__socket)
        except Exception as e:
            logging.debug(f"__selector.unregister() exception for {self.__address}: {repr(e)}")

        try:
            self.__socket.close()
        except OSError as e:
            logging.debug(f"__socket.close() exception for {self.__address}: {repr(e)}")
        finally:
            self.__socket = None
        self.__selector.close()

    @property
    def state(self):
        """Returns the current state of the client."""
        return self.__fsm.state

    def command_init(self, from_state, to_state):
        """Executes the INIT command from the Server. Returns True if the state transition is successful."""
        logging.debug(f"command_init(): {from_state} -> {to_state}")
        self.__proto_message = ProtoMessage.ready_message()
        return True

    def command_update(self, from_state, to_state):
        """Executes the START command from the Server. Returns True if the state transition is successful."""
        logging.debug(f"command_update(): {from_state} -> {to_state}")
        self.__proto_message = ProtoMessage.input_message(["FORWARD", "LEFT", "FIRE"])
        return True

    def command_stop(self, from_state, to_state):
        """Executes the STOP command from the Server. Returns True if the state transition is successful."""
        logging.debug(f"command_stop(): {from_state} -> {to_state}")
        self.stop()
        return True

    def __process_events(self, mask):
        """Processes events."""
        if mask & selectors.EVENT_READ:
            done_reading = self.__reader.read()
            if done_reading:
                self.__process_response(self.__reader.obj)
                self.__reader.reset()
                self.__set_write_mode()

        if mask & selectors.EVENT_WRITE:
            assert self.__proto_message.buffer
            self.__writer.set_buffer(self.__proto_message.buffer)
            done_writing = self.__writer.write()
            logging.debug(f"Sent {self.__proto_message.payload}")

            if done_writing:
                self.__proto_message.reset()
                self.__set_read_mode()

    def __process_response(self, dictionary):
        logging.debug(f"Received response: {dictionary}")
        try:
            self.__fsm.transition(ClientInput(dictionary["message"]))
        except KeyError as e:
            logging.error(f"Bad FSM transition data. {repr(e)}")
        self.__processed_count += 1

    def __set_read_mode(self):
        """Sets __selector to look for read events."""
        self.__selector.modify(self.__socket, selectors.EVENT_READ)

    def __set_write_mode(self):
        """Sets __selector to look for write events."""
        self.__selector.modify(self.__socket, selectors.EVENT_WRITE)


if __name__ == "__main__":
    import time
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(filename)s:%(lineno)d: %(message)s")

    client = Client(("localhost", 54879))
    client.connect("Player2")

    done = False
    while not done:
        try:
            client.tick()
            time.sleep(0.02)

            if client.state == ClientState.PLAYING:
                client.command_update(ClientState.PLAYING, ClientState.PLAYING)

        except (AssertionError, KeyboardInterrupt):
            client.stop()
            done = True

        except ValueError:
            done = True
