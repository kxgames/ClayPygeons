#!/usr/bin/env python

from __future__ import division

import gui
import world

import pygame
from pygame.locals import *

from gui import Gui
from world import World

clock = pygame.time.Clock()

world = World()
gui = Gui(world)

try:
    while world.is_playing():
        time = clock.tick(40) / 1000

        gui.update(time)
        world.update(time)

except KeyboardInterrupt:
    print
