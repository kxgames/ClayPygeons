#!/usr/bin/env python

import settings
import arguments

import pygame
from pygame.locals import *

from world import Universe
from postoffice import Hub, Courier

def main(host, port):

    hub = Hub(host, port, settings.player_count)
    courier = Courier(host, port)
    universe = Universe(courier, settings)

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

    host = arguments.option("host", default=settings.host)
    port = arguments.option("port", default=settings.port, cast=int)

    try:
        main(host, port)
    except KeyboardInterrupt:
        print
