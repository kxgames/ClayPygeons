from __future__ import division

from collisions import *
from connection import *

class Network:

    def __init__(self, world, role, host):
        self.world = world

        if role == "host":
            self.connection = Host(host)
        elif role == "client":
            self.connection = Client(host)
        elif role == "sandbox":
            self.connection = Sandbox(host)
        else:
            assert False

    def setup(self):
        # This will block until a connection is established, so print out a
        # message to let the user know what's going on.
        print "Waiting for a connection to be made..."
        self.connection.enter()
        print "Connection made."

    def update(self, time):
        world = self.world
        connection = self.connection

        map = world.get_map()
        boundary = map.get_size()
        targets = world.get_targets()

        # Find all the targets in this game that have left the field of play,
        # and move them to the other game.
        for target in targets:
            point = target.get_position()

            if not Collisions.point_inside_shape(point, boundary):
                world.remove_target(target)
                connection.send(target)

        # Add any targets that left the other game into this one.
        for target in connection.receive():
            target.wrap_around(boundary)
            world.add_target(target)

    def teardown(self):
        self.connection.exit()

