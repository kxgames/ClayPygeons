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
        #self.react(time)
        self.draw(time)

    def draw(self, time):
        background_color = Color("black")
        sight_color = Color("white")
        target_color = Color("red")

        screen = self.screen
        screen.fill(background_color)

        # First, draw the sight.
        if False:
            sight = self.world.get_sight()
            position = sight.position.pygame

            size = 10; radius = 0.8 * size
            color = sight_color; stroke = 2

            pygame.draw.circle(screen, color, position, radius, stroke)

            up = position + size * Vector(0, -1) / 2
            down = position + size * Vector(0, 1) / 2
            left = position + size * Vector(-1, 0) / 2
            right = position + size * Vector(1, 0) / 2

            pygame.draw.line(screen, color, up.pygame, down.pygame, stroke)
            pygame.draw.line(screen, color, left.pygame, right.pygame, stroke)

        # Second, draw all the targets.
        for target in self.world.get_targets():
            position = target.position.pygame
            radius = target.radius
            color = target_color

            pygame.draw.circle(screen, color, position, radius)
            #pygame.draw.circle(screen, color, position, target.speed, 1)

            #velocity = target.position + target.velocity
            #velocity = velocity.pygame

            #pygame.draw.line(screen, color, position, velocity, 1)

        # Finish the update.
        pygame.display.flip()

    def react(self, time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
            
            if event.type == pygame.JOYAXISMOTION:
                #print 'JOYAXISMOTION   ', event.axis, event.value
                # X axis {{{4
                # Right = 1.0, Left = -1.0
                sight = self.world.get_sight()

                if 0 == event.axis:
                    #joystick_y = self.joystick.get_axis(1)
                    direction = vector.Vector(event.value, 0)
                    sight.accelerate(direction)

                # Y axis {{{4
                # Backwards = 1.0, Forwards = -1.0
                if 1 == event.axis:
                    #joystick_x = self.joystick.get_axis(0)
                    direction = vector.Vector(0, event.value)
                    sight.accelerate(direction)

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

