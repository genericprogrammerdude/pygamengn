from network.replicator import Replicator


class RepicationManager:
    """
    Manages Replicator objects and their associated GameObjects.
    """

    def __init__(self):
        self.__replicators = {}

    def add_replicator(self, replicator, gob):
        """Adds a Replicator object to keep track of."""
        self.__replicators[replicator.id] = {
            "replicator": replicator,
            "game_object": gob
        }
