import sys
import random

import pygame
from pygame.locals import *

from vector import *
from shapes import *
from flocking import *

# Pygame setup {{{1
pygame.init()
boundary = Rectangle.from_size(600, 600)
size = boundary.size
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
frequency = 40

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
cyan = (0,255,255)
purple = (255,0,255)
yellow = (255,255,0)
# }}}1
scenario = 2
# Sprites setup {{{1 
if 1 == scenario:
    # scenario 1: seek flee wander {{{2
    sprites = []
    sprite_radius = 10
    sprite_force = 75
    sprite_speed = 50
    population = 10


    # Make sprites
    for i in range(population):
        sprite_x = boundary.width * random.random()
        sprite_y = boundary.height * random.random()
        sprite_position = Vector(sprite_x,sprite_y)
        sprites.append(Sprite())
        sprites[i].setup(sprite_position, sprite_radius, sprite_force, sprite_speed)

    # Add behaviors to sprites
    for i in range(population):
        vehicle = sprites[i]

        wander_radius = sprite_speed * 2
        wander_distance = sprite_speed / 5.0
        wander_jitter = sprite_speed / 2.0
        if 0 == i:
            leader_target = DummyTarget(boundary.center, 1)
            vehicle.add_behavior (Seek (vehicle, 0.4, leader_target))
            vehicle.add_behavior (Wander (vehicle, 1.0, wander_radius, wander_distance, wander_jitter))
        else:
            seek_target = sprites[i-1]
            if 1 == i:
                seek_radius = 0.0
            else:
                seek_radius = sprite_radius * 15
            vehicle.add_behavior (Seek (vehicle, 2.0, seek_target, seek_radius))
            vehicle.add_behavior (Wander (vehicle, 0.9, wander_radius, wander_distance, wander_jitter))

        #flee_target = sprites[i-2]
        #flee_radius = sprite_radius * 10
        #vehicle.add_behavior (Flee (vehicle, 0.8, flee_target, flee_radius))
    # }}}2
elif 2 == scenario:
    # scenario 2: arrive {{{2
    sprites = []
    dummy_population = 10

    # Make arriver
    arriver_radius = 10
    arriver_force = 100
    arriver_speed = 75
    arriver_x = boundary.width * random.random()
    arriver_y = boundary.height * random.random()
    arriver_position = Vector(arriver_x,arriver_y)

    arriver = Sprite()
    arriver.setup(arriver_position, arriver_radius, arriver_force, arriver_speed)
    sprites.append(arriver)

    # Make dummy targets
    for i in range(dummy_population):
        dummy_x = boundary.width * random.random()
        dummy_y = boundary.height * random.random()
        dummy_position = Vector(dummy_x,dummy_y)
        dummy_radius = 5
        sprites.append(DummyTarget(dummy_position, dummy_radius))

    # Add behaviors to the arriver
    sprites[0].add_behavior(Arrive(sprites[0], 1.0, sprites[1], urgency=0.4))


    # }}}2
# }}}1


while True:
    time = clock.tick(frequency)/1000.0
    # React to Input {{{1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
    screen.fill((0,0,0))

    # Updates {{{1
    for sprite in sprites:
        sprite.update(time)
        #sprite.bounce(time, boundary)
        sprite.wrap_around(boundary)
        if 2 == scenario:
            # scenario 2 changing targets {{{2
            arriver = sprites[0]
            old_behavior = arriver.get_behaviors()[0]
            old_target = old_behavior.get_target()

            distance = arriver.get_position() - old_target.get_position()
            min_distance = arriver.get_radius() + old_target.get_radius()

            if  distance.magnitude <= min_distance:
                old_index = sprites.index(old_target)
                new_index = (old_index +1) % len(sprites)
                if 0 == new_index: new_index += 1
                new_target = sprites[new_index]

                arriver.remove_behavior(old_behavior)
                arriver.add_behavior(Arrive(sprites[0], 1.0, new_target, urgency=0.4))
            # }}}2


    # Draw everything {{{1
    if 1 == scenario:
        # scenario 1 {{{2
        #Draw leader target in the center
        leader_position = sprites[0].get_position()
        leader_radius = sprites[0].get_radius()
        pygame.draw.circle(screen, red, leader_position.pygame, leader_radius)

        #Draw other sprites
        for sprite in sprites:
            position = sprite.get_position()
            radius = sprite.get_radius()

            # Draw circle
            if sprite == sprites[0]:
                pygame.draw.circle(screen, blue, position.pygame, radius, 3)
            else:
                pygame.draw.circle(screen, green, position.pygame, radius, 3)

            # Draw facing direction line
            facing = sprite.get_facing()
            end_point = position + facing * 25
            pygame.draw.line(screen, green, position.pygame, end_point.pygame)

        # Draw force lines for the leader
        if False:
            #sum = Vector.null()
            for behavior in sprites[0].get_behaviors():
                force = behavior.get_last_force()
                #sum += force
                if not force == Vector.null():
                    #force_start = position + force.normal * sprite_radius
                    force_start = sprites[0].get_position()
                    force_end = force + force_start
                    pygame.draw.line(screen, cyan, force_start.pygame, force_end.pygame)
            if False:
                if not sum == Vector.null():
                    sum_start = position + sum.normal *sprite_radius
                    sum_end = sum + sum_start
                    pygame.draw.line(screen, yellow, sum_start.pygame, sum_end.pygame)
        if False:
            # Draw wander circle. Works ONLY if wandering is ONLY behavior
            wander_offset = facing * behavior.d
            wander_radius = behavior.r
            wander_position = wander_offset + position
            pygame.draw.circle(screen, yellow, wander_position.pygame, wander_radius, 1)
            wander_target = behavior.target.get_position() + wander_offset + position
            pygame.draw.circle(screen, red, wander_target.pygame, 5)
        #}}}2
    elif 2 == scenario:
        # scenario 2 {{{2
        # Draw sprites
        for sprite in sprites:
            position = sprite.get_position()
            radius = sprite.get_radius()

            if sprite == sprites[0]:
                # Draw arriver

                # Draw facing direction line
                facing = sprite.get_facing()
                end_point = position + facing * 25
                pygame.draw.line(screen, green, position.pygame, end_point.pygame)

                #Draw circle
                pygame.draw.circle(screen, blue, position.pygame, radius, 3)
            else:
                pygame.draw.circle(screen, green, position.pygame, radius)


        # Draw force lines for the arriver
        if False:
            #sum = Vector.null()
            for behavior in sprites[0].get_behaviors():
                force = behavior.get_last_force()
                #sum += force
                if not force == Vector.null():
                    #force_start = position + force.normal * sprite_radius
                    force_start = sprites[0].get_position()
                    force_end = force + force_start
                    pygame.draw.line(screen, cyan, force_start.pygame, force_end.pygame)
                if False:
                    if not sum == Vector.null():
                        sum_start = position + sum.normal *sprite_radius
                        sum_end = sum + sum_start
                        pygame.draw.line(screen, yellow, sum_start.pygame, sum_end.pygame)
        #}}}2

    pygame.display.flip()
    # }}}1
