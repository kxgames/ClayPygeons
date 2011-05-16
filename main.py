#!/usr/bin/env python

from __future__ import division

import sys
import gui, world, network

from gui import Gui
from world import World
from network import Network

import pygame
from pygame.locals import *

# Decide if the game should be played over a network.
try: role = sys.argv[1]
except IndexError:
    role = "sandbox"

# Figure out how to connect to the network.
try: host = sys.argv[2]
except IndexError:
    host = "localhost"

# Make sure all the arguments make sense.
if role not in ("host", "client", "sandbox"):
    sys.exit("The first argument must be 'host', 'client', or 'sandbox'.")

try:
    world = World()
    systems = [ world, Gui(world), Network(world, role, host) ]

    for system in systems:
        system.setup()

    clock = pygame.time.Clock()
    frequency = 40

    while world.is_playing():
        time = clock.tick(frequency) / 1000
        for system in systems:
            system.update(time)

    for system in systems:
        system.teardown()

except IOError:
    print "A network error caused the game to close unexpectedly."

except KeyboardInterrupt:
    print

