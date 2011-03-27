import sys

import pygame
from pygame.locals import *

import shapes
import vector


class Gui:
    # def __init__ (screen_size, world): {{{1
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
            print pygame.joystick.get_count()

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

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
                #print 'JOYAXISMOTION   ', event.axis, event.value
                # X axis {{{4
                # Right = 1.0, Left = -1.0
                if 0 == event.axis:
                    #joystick_y = self.joystick.get_axis(1)
                    joystick_y = 0
                    acceleration = vector.Vector(event.value, joystick_y)
                    acceleration *= .001
                    sight = self.world.get_sight()
                    sight.set_acceleration(acceleration)

                # Y axis {{{4
                # Backwards = 1.0, Forwards = -1.0
                if 1 == event.axis:
                    #joystick_x = self.joystick.get_axis(0)
                    joystick_x = 0
                    acceleration = vector.Vector(joystick_x, event.value)
                    acceleration *= .001
                    sight = self.world.get_sight()
                    sight.set_acceleration(acceleration)

                # Rotator dial thingy {{{4
                # Down = 1.0, Up = -1.0
                if 2 == event.axis:
                    pass
                #}}}4
            #if event.type == pygame.JOYBALLMOTION:
            #if event.type == pygame.JOYHATMOTION:
            """ 
            if event.type == pygame.JOYBUTTONUP:
                print 'JOYBUTTONUP   ', event.button
            if event.type == pygame.JOYBUTTONDOWN:
                print 'JOYBUTTONDOWN   ', event.button
                """

        sight = self.world.get_sight()
        #print sight.get_position().x
        #print sight.get_position().y
        sight_position = sight.get_position().get_pygame()
        pygame.draw.circle(self.screen, (255, 255, 255), sight_position, 10)

        pygame.display.flip()
        pygame.time.wait(50)

# self.world.get_sight().get_position()
# self.world.get_sight().set_position()
