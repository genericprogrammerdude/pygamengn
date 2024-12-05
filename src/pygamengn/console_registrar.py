import logging


class ConsoleRegistrar:
    """
    Console commands are registered with the ConsoleRegistrar. This allows them to be invoked in the console.
    """

    registry = {}

    @classmethod
    def register(cls, command: str, callback):
        """Registers a new console command."""
        if command in cls.registry:
            logging.warn(f"Command `{command}` is already registered. Select a different command string.")
        else:
            cls.registry[command] = callback

    @classmethod
    def callback(cls, key):
        try:
            return cls.registry[key]
        except KeyError:
            return lambda: f"Error: command `{key}` not found"
