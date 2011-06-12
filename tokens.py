import random
import settings

from vector import *
from collisions import *
from shapes import *
from flocking import *

class Player:

    def __init__(self, address, sight):
        self.address = address
        self.sight = sight
        self.points = 0

    def score(self, points):
        self.points += points

class Map:
    """ Stores information about the game world.  This is just the size of the
    map right now, but it might eventually include information about how
    targets spawn. """

    def __init__(self, world, size):
        self.world = world
        self.size = size

    def update(self, time):
        pass

    def get_size(self):
        return self.size

class Sight(Sprite):
    """ Represents a player's sight.  The motion of these objects is primarily
    controlled by the player, but they will bounce off of walls. """

    def __init__(self, world, position):
        Sprite.__init__(self, position, settings.sight_radius)
        self.world = world

        self.drag = settings.sight_drag
        self.power = settings.sight_power

        self.direction = Vector.null()

    def update(self, time):
        # Set the acceleration.
        force = self.power * self.direction
        drag = -self.drag * self.velocity

        self.acceleration = force + drag
        Sprite.update(self, time)

        # Bounce the sight off the walls.
        boundary = self.world.get_map().get_size()
        Sprite.bounce(self, time, boundary)

    def accelerate(self, direction):
        self.direction = direction

    def shoot(self):
        for target in self.world.targets:
            if Collisions.circles_touching(self.circle, target.circle):
                target.hit()

class Target(Sprite):
    """ Represents a target that players can shoot at.  These objects will
    move autonomously in the final version. """

    def __init__(self, world, position):
        Sprite.__init__(self, position, settings.target_radius)
        self.world = world

        self.power = settings.target_power
        self.speed = settings.target_speed
        self.loopiness = settings.target_loopiness
        self.hitpoints = settings.target_hitpoints

        self.goal = self.speed * Vector.random()

    def update(self, time):
        offset = self.loopiness * Vector.random()

        self.goal = self.goal + offset
        self.goal = self.speed * self.goal.normal

        # The goal is what the velocity should ideally be.  The acceleration
        # can be computed by finding the difference between the current
        # velocity and the goal.
        self.acceleration = self.goal - self.velocity

        # If the acceleration is too fast, then truncate it.
        if self.acceleration.magnitude > self.power:
            self.acceleration = self.power * self.acceleration.normal

        # Update the physics as usual.
        Sprite.update(self, time)

    def hit(self):
        self.hitpoints -= settings.shot_power
        print 'Target hit!', self.hitpoints

    def get_hitpoints(self):
        return self.hitpoints
    
    def get_speed(self):
        return self.speed
