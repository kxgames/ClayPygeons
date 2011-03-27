import settings

from vector import *

class World:
    """ Creates, stores, and provides access to all of the game objects. """

    def __init__(self):
        self.map = Map(self, settings.map_size)
        self.sight = Target(self, setting.target_position)

        self.targets = []
        self.targets_destroyed = []
        self.targets_
        
    def get_map(self):
        return self.map

    def get_sight():
        return self.sight

    def get_targets():
        return self.targets

    def get_

    def update(self, time):
        self.map.update(time)
        self.sight.update(time)

        for target in self.targets:
            target.update(time)

class Map:
    """ Stores information about the game world.  This is just the size of the
    map right now, but it might eventually include information about how
    targets spawn. """

    def __init__(self, world, size):
        self.size = size

    def update(self, time):
        pass

    def get_size(self):
        return self.size

class Sprite:
    """ A parent class for every game object that can move.  This class stores
    position data and handles basic physics, but it is not meant to be
    directly instantiated. """

    def __init__(self, position, velocity, acceleration):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration

    def update(self, time):
        self.velocity += self.acceleration * time
        self.position += self.velocity * time

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_acceleration(self):
        return self.acceleration

    def set_position(self, position):
        self.position = position

    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration

class Sight(Sprite):
    """ Represents a player's sight.  The motion of these objects is promarily
    controlled by the player, but they will bounce off of walls. """

    def __init__(self, world, position):
        Sprite.__init__(self, position, Vector.null(), Vector.null())
        self.world = world

    def update(self, time):
        Sprite.update(time)

        position = self.position
        boundary = self.world.get_map()

        bounce = Vector(1, 1)
        vertical_bounce = Vector(0, -1)
        horizontal_bounce = Vector(-1, 0)

        if position.y < boundary.top or position.y > boundary.bottom:
            bounce = bounce * vertical_bounce

        if position.x < boundary.left or position.x > boundary.right:
            bounce = bounce * horizontal_bounce

        self.velocity = self.velocity * bounce
        self.position = self.velocity * time

class Target(Sprite):
    """ Represents a target that players can shoot at.  These objects will
    move autonomously in the final version. """

    def __init__(self, world):
        Sprite.__init__(self, Vector.null(), Vector.null(), Vector.null())
        self.world = world
