import sys

import pygame
from pygame.locals import *

import shapes
import vector


class Gui:
    # def __init__ (screen_size, world): {{{1
    def __init__ (screen_size, world):
        self.world = world

        pygame.init()

        self.size = screen_size
        screen = pygame.display.set_mode(self.size)

        if pygame.joystick.get_count() == 0:
            print "No joystick! Aborting...."
            sys.exit(0)
        else:
            print pygame.joystick.get_count()

        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    # def update (self, time): {{{1
    def update (self, time):
        screen.fill ((0,0,0))
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
                if event.joy == joystick.get_id():
                    print 'JOYAXISMOTION   ', event.axis, event.value
                    #self.world.
            #if event.type == pygame.JOYBALLMOTION:
            #if event.type == pygame.JOYHATMOTION:
            if event.type == pygame.JOYBUTTONUP:
                if event.joy == joystick.get_id():
                    print 'JOYBUTTONUP   ', event.button
            if event.type == pygame.JOYBUTTONDOWN:
                if event.joy == joystick.get_id():
                    print 'JOYBUTTONDOWN   ', event.button



        pygame.display.flip()
        pygame.time.wait(50)

# self.world.get_sight().get_position()
# self.world.get_sight().set_position()
