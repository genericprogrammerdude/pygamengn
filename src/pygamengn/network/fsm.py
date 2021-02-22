class FiniteStateMachine:
    """A finite state machine class."""

    def __init__(self, state, transitions):
        self.__state = state
        self.__transitions = transitions

    def transition(self, input_enum_value):
        """Executes a transition using the given input."""
        transition_entry = self.__transitions[self.__state][input_enum_value]
        to_state = transition_entry["state"]
        callback = transition_entry.get("callback")
        if (callback and callback(self.__state, to_state)) or callback is None:
            self.__state = to_state
        return self.__state

    @property
    def state(self):
        return self.__state
