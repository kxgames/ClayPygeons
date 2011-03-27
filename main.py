#!/usr/bin/env python

import gui
import world

import pygame
from pygame.locals.import *

from gui import Gui
from world import World

screen = (400, 500)
clock = pygame.time.Clock()

world = World()
gui = Gui(screen, world)

while world.is_playing():
    time = clock.tick(40)

    gui.update(time)
    world.update(time)
