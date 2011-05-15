import pygame
from pygame.locals import *

import vector


class Joystick:
    def __init__ (self, directional_callback):
        pygame.joystick.init()
        
        # Get joystick set up. This code only uses one joystick in the moment.
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        self.x = self.joystick.get_axis(0)
        self.y = self.joystick.get_axis(1)

        self.directional_callback = directional_callback

    def event (self, event):
        # Directional Axis. X, Y {{{4
        # X axis:  Right = 1.0, Left = -1.0
        # Y axis:  Backwards = 1.0, Forwards = -1.0
        if event.axis in (0,1):
            if 0 == event.axis: self.x = event.value
            if 1 == event.axis: self.y = event.value

            direction = vector.Vector (self.x, self.y)
            self.directional_callback (direction)


        # Rotator dial thingy {{{4
        # Down = 1.0, Up = -1.0
        if 2 == event.axis:
            pass


        # Buttons {{{4
        """ 
        if event.type == pygame.JOYBUTTONUP:
            print 'JOYBUTTONUP   ', event.button
        if event.type == pygame.JOYBUTTONDOWN:
            print 'JOYBUTTONDOWN   ', event.button
        """


        # Our joysticks don't have these: {{{4
        #if event.type == pygame.JOYBALLMOTION:
        #if event.type == pygame.JOYHATMOTION:

        #}}}4
