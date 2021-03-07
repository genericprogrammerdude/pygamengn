import struct


class ReplicatedProperty:
    """
    Representation of a GameObject property that is replicated and kept in sync between the server and
    connected clients.
    """

    def __init__(self, name, getter=None, setter=None, packer_class=None):
        self.name = name
        self.getter = getter or name
        self.setter = setter or name
        if packer_class:
            self.packer = packer_class()
        else:
            self.packer = PackerBase()


class PackerBase():
    """Base class for packing/unpacking objects that does no packing."""

    def pack(self, data):
        """Packs data into binary format."""
        return data

    def unpack(self, data):
        """Unpacks data from binary format."""
        return data


class PackerFloat():
    """Class for packing/unpacking floats."""

    def pack(self, data):
        """Packs data into binary format."""
        rv = struct.pack("!f", data).decode("ascii")
        return rv

    def unpack(self, data):
        """Unpacks data from binary format."""
        return struct.unpack("!f", data.encode("ascii"))[0]
