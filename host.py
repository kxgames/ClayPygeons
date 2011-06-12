#!/usr/bin/env python

import pygame
from pygame.locals import *

from world import Universe
from postoffice import Hub, Courier

def main():

    hub = Hub()
    courier = Courier()
    universe = Universe(courier)

    hub.setup()
    courier.setup()

    # This is something of a hacky way to get the post office hub to set up
    # the universe automatically.
    hub.listen(universe.setup)

    clock = pygame.time.Clock()
    frequency = 40

    while universe.still_playing():
        universe.update()
        hub.update(); courier.update()

        clock.tick(frequency)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        print
