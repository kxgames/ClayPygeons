import sys

import pygame
from pygame.locals import *

import shapes
import vector
import joystick


class Gui:
    # def __init__ (self, world): {{{1
    def __init__ (self, world):
        self.world = world
        self.map = self.world.get_map()

        pygame.init()

        self.size = self.map.get_size().get_pygame().size
        self.screen = pygame.display.set_mode(self.size)

        if pygame.joystick.get_count() == 0:
            print "No joystick! Aborting...."
            sys.exit(0)
        else:
            print 'Number of Joysticks:', pygame.joystick.get_count()

        # Make callback dictionary?
        accelerate_callback = self.world.get_sight().accelerate
        self.joystick = joystick.Joystick(accelerate_callback)

    # def update (self, time): {{{1
    def update (self, time):
        self.screen.fill ((0,0,0))
        # Get user input {{{2
        for event in pygame.event.get():
            # Quit {{{3
            if event.type == pygame.QUIT:
                sys.exit(0)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
            
            # Joystick input {{{3
            if event.type == pygame.JOYAXISMOTION:
                self.joystick.event (event)
            # }}}3

        sight = self.world.get_sight()
        #print sight.get_position().x
        #print sight.get_position().y
        sight_position = sight.get_position().get_pygame()
        pygame.draw.circle(self.screen, (255, 255, 255), sight_position, 10)

        pygame.display.flip()
        pygame.time.wait(50)

# self.world.get_sight().get_position()
# self.world.get_sight().set_position()
