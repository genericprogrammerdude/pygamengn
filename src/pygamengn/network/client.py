from enum import Enum, auto

import logging
import selectors
import socket

from network.proto_message import ProtoMessage
from network.proto_reader import ProtoReader
from network.proto_writer import ProtoWriter
from network.fsm import FiniteStateMachine, FSMTransition


class ClientState(Enum):
    DISCONNECTED = auto()
    CONNECTED = auto()
    READY = auto()
    PLAYING = auto()


class ClientInput(Enum):
    CONNECTION_OK = "CONNECTION_OK"
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
        self.__inputs = None
        self.__game_state = {}
        self.__fsm = FiniteStateMachine(ClientState.DISCONNECTED, {
            ClientState.DISCONNECTED: {
                ClientInput.CONNECTION_OK: FSMTransition(ClientState.CONNECTED, self.command_connection_ok)
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

    def reset_game_state(self):
        self.__game_state = {}

    def tick(self):
        """Does client work. Returns True when the connection is alive, False otherwise."""
        if not self.__selector.get_map():
            logging.error("Client ticking but not connected to server. Stopping client.")
            self.stop()
            return False

        events = self.__selector.select(timeout=-1)
        for _, mask in events:
            try:
                self.__process_events(mask)
            except (RuntimeError, ConnectionRefusedError, ConnectionResetError) as e:
                logging.debug(f"Client disconnected: {e}")
                self.stop()
                return False
        return True

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
        except AttributeError:
            pass
        finally:
            self.__socket = None
        self.__selector.close()

    def set_inputs(self, inputs):
        """Sets the list of input actions collected during a frame. These are sent to the server."""
        if self.__fsm.state == ClientState.PLAYING:
            self.__proto_message = ProtoMessage.input_message(inputs)

    def get_game_state(self):
        """Returns the game state dictionary received from the server."""
        return self.__game_state

    @property
    def state(self):
        """Returns the current state of the client."""
        return self.__fsm.state

    def command_connection_ok(self, from_state, to_state, spawn_pos):
        """Executes the INIT command from the Server. Returns True if the state transition is successful."""
        logging.debug(f"command_connection_ok(): {from_state} -> {to_state} spawn_pos = {spawn_pos}")
        self.__proto_message = ProtoMessage.ready_message({
            "game_type": "/Ship",
            "pos": spawn_pos,
            "heading": 0,
            "health": 58
        })
        return True

    def command_update(self, from_state, to_state, objects):
        """Executes the UPDATE command from the Server. Returns True if the state transition is successful."""
        logging.debug(f"command_update(): {from_state} -> {to_state}")
        self.__proto_message = ProtoMessage.input_message(self.__inputs)
        self.__game_state = objects
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
            self.__fsm.transition(
                ClientInput(dictionary["message"]),
                **{key: dictionary[key] for key in dictionary if key != "message"}
            )
        except KeyError as e:
            logging.error(f"Bad FSM transition data. {repr(e)}")
        self.__processed_count += 1

    def __set_read_mode(self):
        """Sets __selector to look for read events."""
        self.__selector.modify(self.__socket, selectors.EVENT_READ)

    def __set_write_mode(self):
        """Sets __selector to look for write events."""
        self.__selector.modify(self.__socket, selectors.EVENT_WRITE)
