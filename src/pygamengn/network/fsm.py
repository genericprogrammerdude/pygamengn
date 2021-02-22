class FiniteStateMachine:
    """A finite state machine class."""

    def __init__(self, state, transitions):
        self.__state = state
        self.__transitions = transitions

    def transition(self, input_enum_value):
        """Executes a transition using the given input."""
        t = self.__transitions[self.__state][input_enum_value]
        if (t.callback and t.callback(self.__state, t.to_state)) or t.callback is None:
            self.__state = t.to_state
        return self.__state

    @property
    def state(self):
        return self.__state


class FSMTransition:
    """Defines a transition for FiniteStateMachine."""

    def __init__(self, to_state, callback=None):
        self.to_state = to_state
        self.callback = callback
