#!/usr/bin/env python

import settings
import arguments

import game, lobby

import protocol
import callbacks

class Lobby(callbacks.Lobby):

    def __init__(self, host, port, name, world):
        self.courier = protocol.Courier(host, port, self)
        self.courier.login(name)

        self.world = world
        self.finished = False

    def update(self):
        self.courier.update()

    def finished(self):
        return self.finished

    def welcome(self, information):
        print information

    def play(self, settings):
        # Use settings to set up the world!

        self.world.

        self.finished = True


if __name__ == "__main__":
    
    # Read several options from the command line.
    name = arguments.first()
    host = arguments.option("host", default=settings.host)
    port = arguments.option("port", default=settings.port, type=int)

    # Construct the core game objects.
    world = World()
    courier = Courier(host, port)
    gui = Gui()

    game = Game(world, courier, gui)

    clock = pygame.time.Clock()
    frequency = 40

    # Connect to the server and ait until enough players have connected.
    # This could take a long time.
    courier.setup()

    # Create the user interface.  Note that this happens after the network
    # is set up, so this game will have a text-based "lobby".
    gui.setup()

    # Enter the game loop and start playing!
    while world.is_playing():
        time = clock.tick(frequency) / 1000
        for system in game:
            system.update(time)

    for system in game:
        system.teardown()

