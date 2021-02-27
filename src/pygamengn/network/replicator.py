class Replicator:
    """
    Every object that needs to be replicated between Client and Server has a Replicator instance.

    Replicator is responsible for maintaining the Client and Server replicas of the same object in sync. It achieves
    this task by taking the values of the replication properties (__properties) on the server and propagating them to
    the connected clients.

    Each connected client will receive the values of the properties from the server and apply them to the local replica
    of the objects that each Replicator instance represents. ReplicationManager will keep a map of replicated game
    objects, using the Replicators' __id fields as unique keys.
    """

    def __init__(self, replicator_id):
        self.__id = replicator_id
        self.__properties = []

    def add_property(self, prop):
        """Adds a property that needs to be replicated."""
        self.__properties.append(prop)

    @property
    def id(self):
        return self.__id
