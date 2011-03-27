import settings

from vector import *

class World:
    """ Creates, stores, and provides access to all of the game objects. """

    def __init__(self):
        self.map = Map(self, settings.map_size)
        self.sight = Sight(self, settings.target_position)

        self.targets = []
        
    def get_map(self):
        return self.map

    def get_sight(self):
        return self.sight

    def get_targets(self):
        return self.targets

    def update(self, time):
        self.map.update(time)
        self.sight.update(time)

        for target in self.targets:
            target.update(time)

    def is_playing(self):
        return True

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

class Sight(Sprite):
    """ Represents a player's sight.  The motion of these objects is promarily
    controlled by the player, but they will bounce off of walls. """

    def __init__(self, world, position):
        Sprite.__init__(self, position, Vector.null(), Vector.null())
        self.world = world

        self.drag = settings.target_drag
        self.power = settings.target_power

        self.direction = Vector.null()

    def update(self, time):
        position = self.position
        boundary = self.world.get_map().get_size()

        bounce = False
        vx, vy = self.velocity

        # Check for collisions against the walls.
        if position.y < boundary.top or position.y > boundary.bottom:
            bounce = True
            vy = -vy

        if position.x < boundary.left or position.x > boundary.right:
            bounce = True
            vx = -vx

        # If there is a bounce, flip the velocity and move back onto the
        # screen.
        if bounce:
            self.velocity = Vector(vx, vy)
            self.position += self.velocity * time

        # Set the acceleration.
        force = self.power * self.direction
        drag = -self.drag * self.velocity

        self.acceleration = force + drag

        # Update the physics as usual.
        Sprite.update(self, time)

    def accelerate(self, direction):
        try:
            self.direction = direction.normal
        except NullVectorError:
            self.direction = Vector.null()

class Target(Sprite):
    """ Represents a target that players can shoot at.  These objects will
    move autonomously in the final version. """

    def __init__(self, world):
        Sprite.__init__(self, Vector.null(), Vector.null(), Vector.null())
        self.world = world
