import sys
import joystick

import pygame
from pygame.locals import *

from shapes import *
from vector import *

from tokens import Snitch

class Gui:
    # def __init__(self, world): {{{1
    def __init__ (self, courier, world):
        self.courier = courier
        self.world = world

    # def setup(self): {{{1
    def setup(self):
        self.map = self.world.get_map()

        pygame.init()

        self.size = self.map.get_size().get_pygame().size
        self.screen = pygame.display.set_mode(self.size)

        self.font = pygame.font.Font(None, 20)

        if pygame.joystick.get_count() == 0:
            print "No joystick! Aborting...."
            sys.exit(0)
        else:
            print 'Number of Joysticks:', pygame.joystick.get_count()

        # Callback dictionary for joystick event handling.
        joystick_callbacks = {
                'direction' : self.world.get_sight(0).accelerate,
                'shoot' : self.world.get_sight(0).shoot }

        self.joystick = joystick.Joystick(joystick_callbacks)

    # def teardown(self): {{{1
    def teardown(self):
        pass

    # def update(self, time): {{{1
    def update(self, time):
        self.react(time)
        self.draw(time)

    # def draw(self, time): {{{1
    def draw(self, time):
        background_color = Color("black")
        sight_color = Color("white")

        quaffle_color = Color("red")
        snitch_color = Color("yellow")

        text_color = Color("green")

        screen = self.screen
        screen.fill(background_color)

        # First, draw all the targets in the background.
        for target in self.world.get_targets():
            position = target.get_position()
            radius = target.get_radius()
            color = snitch_color if isinstance(target, Snitch) else quaffle_color

            pygame.draw.circle(screen, color, position.pygame, radius)

            # Draw a hitpoint bar
            hp_ratio = target.get_health()

            bar_width = hp_ratio * 2 * radius
            bar_height = 2

            delta = Vector(-radius, -(radius + 2 * bar_height))
            bar_position = (position + delta).pygame

            hp_bar = Rect(bar_position, (bar_width, bar_height))

            pygame.draw.rect(screen, (255,0,0), hp_bar)

            # Draw the velocity and acceleration vectors.
            velocity = target.get_velocity()
            if velocity.magnitude>0:
                velocity_start = velocity.normal * (radius + 5) + position
                velocity_end = velocity_start + velocity * 5
                pygame.draw.line(screen, (0,0,255), velocity_start.pygame,
                    velocity_end.pygame)

            acceleration = target.get_behavior_acceleration()
            if acceleration.magnitude>0:
                acceleration_start = acceleration.normal * (radius + 5) + position
                acceleration_end = acceleration_start + acceleration * 5
                pygame.draw.line(screen, (0,255,0), acceleration_start.pygame,
                        acceleration_end.pygame)

            # Draw the number of points this target is worth.
            points = str(target.get_points())
            text = self.font.render(points, True, text_color)

            screen.blit(text, position.pygame)

        # After that, draw the sight in the foreground.
        sight = self.world.get_sight(0)
        position = sight.get_position().pygame

        # If the size of the sight is made too small, it starts to look
        # asymmetric.  This probably has to do with the float-to-int
        # conversion and won't be easy to fix.  So stick with large sights.
        radius = 5 * sight.get_size() + 10; size = int(1.25 * radius)
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

