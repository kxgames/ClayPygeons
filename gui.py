import sys

import pygame
from pygame.locals import *

from shapes import *
from vector import *

import settings
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

        # Callback dictionary for joystick event handling.
        joystick_callbacks = {
                'direction' : self.world.get_sight().accelerate,
                'shoot' : self.world.get_sight().shoot
                }

        self.joystick = joystick.Joystick(joystick_callbacks)

    # def update(self, time): {{{1
    def update (self, time):
        self.react(time)
        self.draw(time)

    # def draw(self, time): {{{1
    def draw(self, time):
        background_color = Color("black")
        sight_color = Color("white")
        target_color = Color("red")

        screen = self.screen
        screen.fill(background_color)

        # First, draw all the targets in the background.
        for target in self.world.get_targets():
            position = target.get_position().pygame
            radius = target.get_radius()
            color = target_color

            pygame.draw.circle(screen, color, position, radius)

        # Second, draw the sight in the foreground.
        sight = self.world.get_sight()
        position = sight.get_position().pygame

        # If the size of the sight is made to small, it starts to look
        # asymmetric.  This probably has to do with the float-to-int
        # conversion and won't be easy to fix.  So stick with large sights.
        radius = settings.sight_radius; size = int(1.25 * radius)
        color = sight_color; stroke = 2

        pygame.draw.circle(screen, color, position, radius, stroke)

        up = sight.get_position() + size * Vector(0, -1)
        down = sight.get_position() + size * Vector(0, 1)
        left = sight.get_position() + size * Vector(-1, 0)
        right = sight.get_position() + size * Vector(1, 0)

        pygame.draw.line(screen, color, up.pygame, down.pygame, stroke)
        pygame.draw.line(screen, color, left.pygame, right.pygame, stroke)

        # Finish the update.
        pygame.display.flip()

    # def react(self, time): {{{1
    def react(self, time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
            
            if event.type == pygame.JOYAXISMOTION:
                self.joystick.axis_event(event)

            if event.type == pygame.JOYBUTTONDOWN:
                self.joystick.button_event(event, True)

            if event.type == pygame.JOYBUTTONUP:
                self.joystick.button_event(event, False)
            # }}}3

