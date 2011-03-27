#!/usr/bin/env python

import gui
import world

import pygame
from pygame.locals.import *

from gui import Gui
from world import World

clock = pygame.time.Clock()

world = World()
gui = Gui(screen, world)
network = Network(world)

while world.is_playing():
    time = clock.tick(40)

    gui.update(time)
    world.update(time)
