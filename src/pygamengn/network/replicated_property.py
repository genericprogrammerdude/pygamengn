class ReplicatedProperty:
    """
    Representation of a GameObject property that is replicated and kept in sync between the server and
    connected clients.
    """

    def __init__(self, name, getter=None, setter=None):
        self.name = name
        self.getter = getter or name
        self.setter = setter or name
