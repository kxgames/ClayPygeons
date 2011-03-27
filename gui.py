import sys

import pygame
from pygame.locals import *

pygame.init()

size = 500, 500
screen = pygame.display.set_mode(size)

#pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print "No joystick! Aborting...."
    sys.exit(0)
else:
    print pygame.joystick.get_count()

joystick = pygame.joystick.Joystick(0)
joystick.init()

while True:
    screen.fill ((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
        
        if event.type == pygame.JOYAXISMOTION:
            if event.joy == joystick.get_id():
                print 'JOYAXISMOTION   ', event.axis, event.value
        if event.type == pygame.JOYBALLMOTION:
            if event.joy == joystick.get_id():
                print 'JOYBALLMOTION   ', event.ball, event.rel
        #if event.type == pygame.JOYHATMOTION:
            #if event.joy == joystick.get_id():
                #print 'JOYHATMOTION   ', event.hat, event.value
        if event.type == pygame.JOYBUTTONUP:
            if event.joy == joystick.get_id():
                print 'JOYBUTTONUP   ', event.button
        if event.type == pygame.JOYBUTTONDOWN:
            if event.joy == joystick.get_id():
                print 'JOYBUTTONDOWN   ', event.button

    pygame.display.flip()
    pygame.time.wait(50)
