import pygame
from pygame.locals import *

import vector
import output

class Joystick:
    def __init__ (self, callbacks):
        pygame.joystick.init()
        
        # Get joystick set up. This code only uses one joystick in the moment.
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        with output.NoPrint():
            self.x = self.joystick.get_axis(0)
            self.y = self.joystick.get_axis(1)

        self.callbacks = callbacks

    # def axis_event (self, event): {{{1
    def axis_event (self, event):
        # Directional Axis. X, Y {{{2
        # X axis:  Right = 1.0, Left = -1.0
        # Y axis:  Backwards = 1.0, Forwards = -1.0
        if event.axis in (0,1):
            if 0 == event.axis: self.x = event.value
            if 1 == event.axis: self.y = event.value

            direction = vector.Vector (self.x, self.y)
            self.callbacks['direction'] (direction)

        # Rotator dial thingy {{{2
        # Down = 1.0, Up = -1.0
        if 2 == event.axis:
            pass
        #}}}2


    # def button_event (self, event):{{{1
    def button_event (self, event, down):
        # down is True when event is button down. False if event is button up.
        if down:
            if event.button == 0:
                self.callbacks['shoot'] ()

    # Our joysticks don't have these: {{{1
    #if event.type == pygame.JOYBALLMOTION:
    #if event.type == pygame.JOYHATMOTION:

    #}}}1
