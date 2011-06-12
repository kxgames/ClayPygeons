#!/usr/bin/env python

from gui import Gui
from world import World
from postoffice import Courier

import pygame
from pygame.locals import *

def main():

    # Construct the objects that will run the game.
    courier = Courier()
    world = World(courier)
    gui = Gui(courier, world)

    systems = [courier, world, gui]

    # Connect to the server and wait until the game is ready to begin.
    courier.setup()
    courier.login(world.setup)

    # Open up a window and get ready to start playing.
    clock = pygame.time.Clock()
    frequency = 40

    gui.setup()
    
    # Play the game!
    while world.still_playing():
        time = clock.tick(frequency) / 1000
        for system in systems:
            system.update(time)

    # Exit gracefully.
    for system in systems:
        system.teardown()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print
